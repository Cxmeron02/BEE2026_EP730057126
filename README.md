# U.S Stock Market Empirical Project

This is the repository for my empirical project for BEE2041. This project investigates the evolution of the U.S stock market in the years post-financial crisis, focusing on comparing performance of different sectors as well as the growth of ETF trading activity and passive investment strategies. 

# Repository structure

```text
BEE2026_EP730057126/
│
├– blogpost/                   # Final blog post
│   └── stock_market_blog.ipynb
│
├– data/
│   ├── raw/                   # Downloaded and scraped datasets
│   └── cleaned/               # Processed datasets used in analysis
│
├– outputs/
│  ├── figures/                # Saved charts and tables for blog post 
│  └── tables/                 # Processed data files used to generate figures for blog post
│
├– scripts/
│  ├── cleandata.py            # Clean and extract data necessary for analysis
│  ├── datanalysis.py          # Calculate statistics and manipulating data for figures
│  ├── graphgen.py             # Create final figures for blog post
│  ├── harvestdata.py          # Download raw data 
│  └── scrapedata.py           # Webscrape S&P 500 data
│
├── README.md
└── requirements.txt
```

# Data sources

```text
1) Yahoo Finance 

– Provides data for sector ETFs (XLK, XLF, XLE, XLV, SPY), to use as proxy values for the wider, respective sector performance.

2) Wikipedia S&P 500 List
3) Slickchart S&P 500 List

– Combine to generate a full list of firms listed on S&P 500, containing their respective sector classification and market weights.
```

# Required Python libraries 

Run this in terminal to ensure all required packages are downloaded

```bash 
pip install -r requirements.txt
```

# Project replication order

Run these scripts in the following order in Terminal:

```bash
python harvestdata.py
python scrapedata.py
python cleandata.py
python dataanalysis.py
python graphgen.py
```
The final blog post can be viewed in: blogpost/blog.ipynb

# Further Notes

Some of my earlier git commits may seem pointless at first glance with very little changes. This is beacuse I was having issues early on with accessing the correct local repository and committing to GitHub, and therefore was simply testing to see whether or not I had finally solved this issue. 
