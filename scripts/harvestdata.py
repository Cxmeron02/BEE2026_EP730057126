import yfinance as yfin

print("Gathering ETF data from Yahoo Finance...")


# Create a list of ETF tickers to identify sector proxies
etf_tickers = ["XLK", "XLF", "XLE", "XLV", "SPY"]

# Establish time range for data retrieval.
start_date = "2010-01-01"
end_date = "2025-12-31"

for etf_ticker in etf_tickers:
    print(f"Currently downloading: {etf_ticker}")

    data = yfin.download(etf_ticker, start=start_date, end=end_date)

    # Check for any empty datasets
    if data.empty:
        print(f"Failed: No data available for {etf_ticker}")
        continue

    # Save the data as a CSV file
    filename = f"data/raw/{etf_ticker}.csv"
    data.to_csv(filename)

    print(f"Downloaded and Saved: {filename}")

print("Finished downloading ETF data from Yahoo Finance")