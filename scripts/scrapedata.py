import pandas as pd
import requests
from io import StringIO

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Referer": "https://www.google.com/"
}

print("Scraping S&P 500 data...")

# Wikipedia data
wiki_url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
wiki_response = requests.get(wiki_url, headers=headers, timeout=30)
wiki_response.raise_for_status()

wiki_data = pd.read_html(StringIO(wiki_response.text))

# Select first table form Wikipedia page
wiki_table = wiki_data[0]

# Select relevant columns for future analysis
wiki_table = wiki_table[["Symbol", "Security", "GICS Sector"]].copy()


print("Wikipedia S&P500 data succesfully collected")

# Slickcharts data
slickchart_url = "https://www.slickcharts.com/sp500"
slickchart_response = requests.get(slickchart_url, headers=headers, timeout=30)
slickchart_response.raise_for_status()

slickchart_data = pd.read_html(StringIO(slickchart_response.text))

slickchart_table = slickchart_data[0]

# Keep relevant columns
slickchart_table = slickchart_table[["#", "Company", "Symbol", "Weight"]].copy()

# Rename columns
slickchart_table.columns = ["Rank", "Company", "Symbol", "Weight (%)"]

# Clean weight column
slickchart_table["Weight (%)"] = slickchart_table["Weight (%)"].str.replace("%", "", regex=False)
slickchart_table["Weight (%)"] = pd.to_numeric(slickchart_table["Weight (%)"])

print("Slickcharts S&P500 data successfully collected")

#   Merge datasets
merged_data = pd.merge(
    slickchart_table,
    wiki_table,
    on="Symbol",
    how="left"
)

print("New merged dataset created with Wikipedia and Slickcharts data")

# Reorder columns for readability/logic

merged_data = merged_data[
    ["Rank", "Symbol", "Security", "Company", "GICS Sector", "Weight (%)"]
]

# Save output

SP500_file = "data/raw/sp500_combined.csv"
merged_data.to_csv(SP500_file, index=False)

print(f"Saved combined dataset to {SP500_file}")