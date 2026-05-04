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

#1) Normalising sector performance over set period

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

# Section 4: Calculating cumulative returns for each ETF over the period.

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

