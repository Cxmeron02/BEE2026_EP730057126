# BEE2026_EP730057126
This is the repository for my empirical project for BEE2041. The purpose of this project is to investigate the evolution of the U.S stock market in the years since the financial crisis, focusing on comparing performance of different sectors as well as the growth of ETF trading activity and passive investment strategies. 

# Repository structure/directory

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
Yahoo Finance (ETFs: XLK, XLF, XLE, XLV, SPY)
Wikipedia S&P 500 List
Slickchart S&P 500 List
```

# Required Python libraries 

Run this in terminal to ensure all required packages are downloaded

```bash 

pip install requirements.txt

```

# Project replication order

Run these scripts in the follwoing order:

```bash

python scrapedata.py
python harvestdata.py
python cleandata.py
python dataanalysis.py
python graphgen.py

```