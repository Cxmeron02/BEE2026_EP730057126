import pandas as pd
import matplotlib.pyplot as plt

# Load datasets from dataanalysis.py
normalised_prices = pd.read_csv("outputs/tables/normalised_prices.csv")
cumulative_returns = pd.read_csv("outputs/tables/cumulative_returns.csv")
risk_return_summary = pd.read_csv("outputs/tables/risk_return_summary.csv")
sector_weight_summary = pd.read_csv("outputs/tables/sector_weight_summary.csv")
volume_ratio = pd.read_csv("outputs/tables/volume_ratio.csv")

print("\nGenerating graphs...")

# Convert "Date" columns to datetime format for plotting.
normalised_prices["Date"] = pd.to_datetime(normalised_prices["Date"])
cumulative_returns["Date"] = pd.to_datetime(cumulative_returns["Date"])
volume_ratio["Date"] = pd.to_datetime(volume_ratio["Date"])

# Figure 1: Normalised ETF performance over set period
normalised_prices.plot(
    x="Date",
    y=["XLK_Close", "XLF_Close", "XLE_Close", "XLV_Close", "SPY_Close"]
    ,linewidth=1.5
    , linestyle=":"
)

plt.title("Normalised ETF Performance (2010–2025), Index value = 100")
plt.xlabel("Year")
plt.ylabel("Index price ($)")
plt.grid(alpha=0.75)
plt.savefig("outputs/figures/figure1_normalised_performance.png")
plt.close()

# Figure 2: Cumulative returns over time

cumulative_returns_pct = cumulative_returns.copy()

for col in ["XLK_Close", "XLF_Close", "XLE_Close", "XLV_Close", "SPY_Close"]:
    cumulative_returns_pct[col] = ((cumulative_returns_pct[col] - 1) * 100)


cumulative_returns_pct.plot(
    x="Date",
    y=["XLK_Close", "XLF_Close", "XLE_Close", "XLV_Close", "SPY_Close"]
    ,linestyle=":"
    ,linewidth=1.5
)

plt.title("Cumulative Returns by ETF (2010–2025)")
plt.xlabel("Date")
plt.ylabel("Cumulative Returns (%)")
plt.grid(alpha=0.75)
plt.savefig("outputs/figures/figure2_cumulative_returns.png")
plt.close()

# Figure 3: Sector index weight distribution within the S&P 500

plt.figure(figsize=(8, 8))
plt.pie(
    sector_weight_summary["Total Weight (%)"],
    labels=sector_weight_summary["GICS Sector"],
    autopct="%1.1f%%",
    startangle=140,
    labeldistance=1.21,
    pctdistance=1.11,
    textprops={'fontsize': 8}
)

plt.title("S&P500 Sector Weight Distribution (2025)")
plt.tight_layout()
plt.savefig("outputs/figures/figure3_sector_weight.png")
plt.close()

# Figure 4: Number of S&P 500 firms by sector
sector_counts = sector_weight_summary[["GICS Sector", "Company Count"]]

sector_counts = (sector_counts.sort_values(by="Company Count", ascending=False).reset_index(drop=True))

sector_counts.to_csv("outputs/tables/sector_company_counts.csv", index=False)


fig, ax = plt.subplots()
ax.axis("off")

table = ax.table(
    cellText=sector_counts.values,
    colLabels=sector_counts.columns,
    cellLoc="center",
    loc="center"
)
table.scale(1, 1.5)

plt.title("S&P 500 Company Count by Sector")
plt.savefig("outputs/figures/figure4_sector_counts_table.png")
plt.show()
plt.close()

# Figure 5: Annualised returns by ETF

# Convert to percentage form for easier interpretation
risk_return_summary["Annualised Return (%)"] = (risk_return_summary["Annualised Return"] * 100)

risk_return_summary.plot(
    x="ETF",
    y="Annualised Return (%)",
    kind="bar",
    legend=False
)

plt.title("Average Annual Returns of Sector ETFs (2010–2025)")
plt.xlabel("ETF")
plt.ylabel("Annual return (%)")
plt.tight_layout()
plt.savefig("outputs/figures/figure5_annualised_returns.png")
plt.close()

# Figure 6: Annualised volatility by ETF

# Convert to percentage form for easier interpretation
risk_return_summary["Annualised Volatility (%)"] = (risk_return_summary["Annualised Volatility"] * 100)

risk_return_summary.plot(
    x="ETF",
    y="Annualised Volatility (%)",
    kind="bar",
    legend=False
)

plt.title("Annualised Volatility by Sector ETFs (2010–2025)")
plt.xlabel("ETF")
plt.ylabel("Annual volatility (%)")
plt.tight_layout()
plt.savefig("outputs/figures/figure6_annualised_volatility.png")
plt.close()

# Figure 7: Risk-return scatter plot

# Convert both annualised return and volatility to percentages for better visualisation.
risk_return_summary["Annualised Return (%)"] = (risk_return_summary["Annualised Return"] * 100)
risk_return_summary["Annualised Volatility (%)"] = (risk_return_summary["Annualised Volatility"] * 100)

plt.scatter(
    risk_return_summary["Annualised Volatility (%)"],
    risk_return_summary["Annualised Return (%)"]
)

for i in range(len(risk_return_summary)):
    plt.text(
        risk_return_summary["Annualised Volatility (%)"][i],
        risk_return_summary["Annualised Return (%)"][i]+ 0.1,
        risk_return_summary["ETF"][i],
        fontsize=8,
    )

plt.title("Risk vs Return by ETF (2010–2025)")
plt.xlabel("Annualised volatility (%)")
plt.ylabel("Annualised return (%)")
plt.grid(alpha=0.75)
plt.tight_layout()
plt.savefig("outputs/figures/figure7_risk_return_scatter.png")
plt.close()

# Figure 8: ETF volume relative to SPY

volume_ratio_smooth = volume_ratio.copy()

# Taking 63 as number of trading days in a quarter (252 divided by 4) to smooth the volume ratio data. 
volume_ratio_smooth["XLK_to_SPY"] = volume_ratio_smooth["XLK_to_SPY"].rolling(63).mean()
volume_ratio_smooth["XLF_to_SPY"] = volume_ratio_smooth["XLF_to_SPY"].rolling(63).mean()
volume_ratio_smooth["XLE_to_SPY"] = volume_ratio_smooth["XLE_to_SPY"].rolling(63).mean()
volume_ratio_smooth["XLV_to_SPY"] = volume_ratio_smooth["XLV_to_SPY"].rolling(63).mean()

volume_ratio_smooth.plot(
    x="Date",
    y=["XLK_to_SPY", "XLF_to_SPY", "XLE_to_SPY", "XLV_to_SPY"],
    linewidth =1.1,
)

plt.title("Sector ETF Trading Activity Relative to SPY")
plt.xlabel("Date")
plt.ylabel("Volume ratio")
plt.tight_layout()
plt.savefig("outputs/figures/figure8_volume_ratio.png")
plt.show()
plt.close()

print("\nAll figures saved to outputs/figures")



