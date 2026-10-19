# **Visualizing Stock Performance and Revenue Data**

This project focuses on analyzing and visualizing the historical stock performance and revenue data for selected companies. Using Python, it integrates financial data from Yahoo Finance and revenue data scraped from web sources, then creates interactive visualizations to compare trends.

## **Key Features:**

- Fetches stock price data using the `yfinance` library.
- Extracts revenue data from HTML tables with `BeautifulSoup`.
- Cleans and processes the data for accurate analysis.
- Generates dual-panel visualizations using `Plotly`:
  - Top panel: Historical share prices.
  - Bottom panel: historical quarterly revenue on a numeric (to-scale) axis.
  - ![image](https://github.com/user-attachments/assets/3bb340d9-8dae-45ec-a6dd-3432fa696174)
- Interactive features include zooming, panning, and a date range slider. 

This project provides a streamlined way to explore and understand the financial trends of companies like Tesla and GameStop.

## Method notes (logic fixes)

- Revenue is parsed into **numbers** ($US millions) and real dates (`revenue.py`). It used to be plotted as text, which gave a categorical, not-to-scale axis that `autorange="reversed"` hid.
- The revenue tables are found by their header ("Quarterly Revenue"), not by position on the page.
- Charts cover the date range **both** series have. The old hard-coded cut-offs are gone; they were hiding Tesla's last 6 quarters (2021-06 to 2022-09).
- The revenue is a frozen IBM course snapshot (Tesla to 2022-09-30, GameStop to 2020-04-30). Prices are live and split/dividend-adjusted, and the charts are labelled that way.
- Run `pytest tests` to test (needs network; requirements: yfinance, pandas, requests, beautifulsoup4, plotly, nbformat, nbclient, ipykernel, pytest).
