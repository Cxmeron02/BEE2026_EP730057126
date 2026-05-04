import pandas as pd

print("\nCleaning raw dataset .csv files for useful and insightful analysis")

# Section 1: Load and clean ETF CSV files

# Create new empty dataframes to store cleaned price and volume data for all 5 ETFs.
price_data = pd.DataFrame()
volume_data = pd.DataFrame()

etf_tickers = ["XLK", "XLF", "XLE", "XLV", "SPY"]

for etf_ticker in etf_tickers:

    print(f"Cleaning {etf_ticker} data")

    file = f"data/raw/{etf_ticker}.csv"

    dataset = pd.read_csv(file, skiprows=[1,2])
    dataset = dataset.rename(columns={"Price": "Date"})

    # Keep required columns
    dataset = dataset[["Date", "Close", "Volume"]]

    # Rename selected columns for new dataset for clarity
    dataset = dataset.rename(columns={
        "Close": f"{etf_ticker}_Close",
        "Volume": f"{etf_ticker}_Volume"
    })

    # Remove all rows with any missing values
    dataset = dataset.dropna()
    # Ensure all values are in chronological order
    dataset = dataset.sort_values(by="Date")

    # Merge daily closing price data by date
    if price_data.empty:
        price_data = dataset[["Date", f"{etf_ticker}_Close"]]
    else:
        price_data = pd.merge(
            price_data,
            dataset[["Date", f"{etf_ticker}_Close"]],
            on="Date",
            how="inner"
        )

        # Merge data for total number of shares traded by date
    if volume_data.empty:
        volume_data = dataset[["Date", f"{etf_ticker}_Volume"]]
    else:
        volume_data = pd.merge(
            volume_data,
            dataset[["Date", f"{etf_ticker}_Volume"]],
            on="Date",
            how="inner"
        )

# Save cleaned ETF datasets
price_data.to_csv("data/cleaned/prices_clean.csv", index=False)
volume_data.to_csv("data/cleaned/volume_clean.csv", index=False)

print("\nCleaned ETF price and volume datasets saved")

# Section 2: Clean scraped S&P500 dataset

print("\nCleaning scraped S&P 500 dataset...")

sp500 = pd.read_csv("data/raw/sp500_combined.csv")

# Check missing values
print("\nMissing values before cleaning:")
print(sp500.isna().sum())

# Remove all rows with missing sector information.
sp500 = sp500.dropna(subset=["GICS Sector"])

# Remove extra spaces from text columns to ensure consistency.
sp500["Symbol"] = sp500["Symbol"].str.strip()
sp500["Security"] = sp500["Security"].str.strip()
sp500["Company"] = sp500["Company"].str.strip()
sp500["GICS Sector"] = sp500["GICS Sector"].str.strip()

# Check for any duplicate company names
print("\nDuplicate company names before grouping:")
print(sp500["Company"].duplicated().sum())

# Combine any duplicate company rows by summing their weight. 
sp500_cleaned = sp500.groupby(
    ["Company", "GICS Sector"],
    as_index=False
)["Weight (%)"].sum()

sp500_cleaned = sp500_cleaned.sort_values(by="Weight (%)", ascending=False)

# Save cleaned row-level S&P500 dataset to data/cleaned folder
sp500_cleaned.to_csv("data/cleaned/sp500_cleaned.csv", index=False)
print("\nCleaned S&P 500 table saved")

# Section 3: Check for any remaining errors or inconsistencies in the cleaned datasets.

print("\nFinal cleaned ETF price and volume data:")
print(price_data.head())
print(volume_data.head())

print("\nFinal cleaned S&P 500 company weights:")
print(sp500_cleaned.head())