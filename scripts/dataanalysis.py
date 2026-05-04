import pandas as pd
import numpy as np

# Load cleaned datasets

print("\nAnalysing cleaned datasets...")
prices = pd.read_csv("data/cleaned/prices_clean.csv")
volumes = pd.read_csv("data/cleaned/volume_clean.csv")
sp500 = pd.read_csv("data/cleaned/sp500_cleaned.csv")
print("\nCleaned datasets loaded")

# Convert "Date" column in both datasets to datetime format for analysis.
prices["Date"] = pd.to_datetime(prices["Date"])
volumes["Date"] = pd.to_datetime(volumes["Date"])

#1) Normalising sector performance to compare relative ETF performance over set period 

price_columns = ["XLK_Close", "XLF_Close", "XLE_Close", "XLV_Close", "SPY_Close"]

normalised_prices = prices.copy()

for column in price_columns:
    normalised_prices[column] = (normalised_prices[column] / normalised_prices[column].iloc[0]) * 100

normalised_prices.to_csv("outputs/tables/normalised_prices.csv", index=False)

print("\nNormalised price data saved")

#2) Calulating daily returns for each ETF over the period.

daily_returns = prices.copy()

for column in price_columns:
    daily_returns[column] = daily_returns[column].pct_change()

daily_returns = daily_returns.dropna()

daily_returns.to_csv("outputs/tables/daily_returns.csv", index=False)

print("\nDaily returns data saved")

#3) Calculating cumulative returns for each ETF over the period.

cumulative_returns = daily_returns.copy()
for column in price_columns:

    cumulative_returns[column] = cumulative_returns[column].fillna(0)

    # Create empty list to store cumulative return values and set initial value to 1 (initial investment)
    cumulative_values = []
    current_value = 1

    for r in cumulative_returns[column]:
        current_value = current_value * (1 + r)
        # Convert value back into return form i.e subtract 1 to get the return percentage and append to empty list
        cumulative_values.append(current_value - 1)
        
    cumulative_returns[column] = cumulative_values

cumulative_returns.to_csv("outputs/tables/cumulative_returns.csv", index=False)
print("\nCumulative returns data saved")

#4) Risk-return summary

# Create empty list to store summary data for each ETF
summary_data = []

for column in price_columns:
    average_daily_return = daily_returns[column].mean()
    annualised_return = average_daily_return * 252
    annualised_volatility = daily_returns[column].std() * np.sqrt(252)

    summary_data.append([
        column,
        average_daily_return,
        annualised_return,
        annualised_volatility]
        )

risk_return_summary = pd.DataFrame(
    summary_data,
    columns=[
        "ETF",
        "Average Daily Return",
        "Annualised Return",
        "Annualised Volatility"]
        )

# Remove "_Close" from ETF names for simplicity
risk_return_summary["ETF"] = risk_return_summary["ETF"].str.replace("_Close", "")

risk_return_summary.to_csv("outputs/tables/risk_return_summary.csv", index=False)
print("\nRisk-return summary saved")

#5: Sector weight and company count summary

print("\nCreating sector weight summary...")

# Count number of companies in each sector
company_count = sp500.groupby(
    "GICS Sector",
    as_index=False
    )["Company"].count()

# Rename column for clarity
company_count = company_count.rename(columns={"Company": "Company Count"})

# Calculate total weight for each sector
sector_weights = sp500.groupby("GICS Sector", as_index=False)["Weight (%)"].sum()

# Rename column for clarity
sector_weights = sector_weights.rename(columns={"Weight (%)": "Total Weight (%)"})

# Merge on the "GICS Sector" column
sector_weight_summary = pd.merge(
    company_count,
    sector_weights,
    on="GICS Sector"
)

#Order by "Total Weight (%)" in descending order.  
sector_weight_summary = sector_weight_summary.sort_values(by="Total Weight (%)", ascending=False)

sector_weight_summary.to_csv("outputs/tables/sector_weight_summary.csv",index=False)
print("\nSector weight summary dataset saved")

#6: ETF/SPY volume ratio

volume_ratio = volumes[["Date"]].copy()

volume_ratio["XLK_to_SPY"] = volumes["XLK_Volume"] / volumes["SPY_Volume"]
volume_ratio["XLF_to_SPY"] = volumes["XLF_Volume"] / volumes["SPY_Volume"]
volume_ratio["XLE_to_SPY"] = volumes["XLE_Volume"] / volumes["SPY_Volume"]
volume_ratio["XLV_to_SPY"] = volumes["XLV_Volume"] / volumes["SPY_Volume"]

volume_ratio.to_csv("outputs/tables/volume_ratio.csv", index=False)

print("\nVolume ratio data saved")

# Final checks
print("\nNormalised prices:")
print(normalised_prices.head(5))

print("\nDaily returns:")
print(daily_returns.head(5))

print("\nRisk-return summary:")
print(risk_return_summary)

print("\nSector weight summary:")
print(sector_weight_summary.head(5))

print("\nVolume ratio:")
print(volume_ratio.head(5))