# Stock Market Data Pipeline

An end-to-end ETL data pipeline that fetches historical stock price data for Philippine-linked companies using yfinance, stores it in a SQLite database, computes financial metrics, and presents insights through an interactive Streamlit dashboard with Plotly charts.

---

## Dashboard Preview

> Run the dashboard locally to interact with live stock data.

---

## Stocks Tracked

| Ticker | Company | Market | Currency |
|---|---|---|---|
| SM.PS | SM Investments Corporation | PSE | PHP |
| JBFCY | Jollibee Foods Corporation | OTC | USD |
| BDOUY | BDO Unibank Inc | OTC | USD |

> Note: SM.PS is priced in PHP. JBFCY and BDOUY are US OTC listings priced in USD.

---

## Features

- Fetches historical OHLCV data for 3 stocks using yfinance
- Stores raw and transformed data in a structured SQLite database
- Computes 8 financial metrics per stock per day
- Interactive dashboard with stock selector dropdown
- Candlestick, volume, daily return, volatility, and comparison charts
- SQL-powered analysis across two normalized database tables

---

## Tech Stack

| Layer | Tool |
|---|---|
| Language | Python 3 |
| Data source | yfinance (Yahoo Finance) |
| Data manipulation | pandas |
| Database | SQLite via sqlite3 |
| Visualization | Plotly, Streamlit |
| Automation | Windows Task Scheduler + .bat script |

---

## Project Structure

```
stock-pipeline/
├── scripts/
│   ├── extract_stocks.py        # Fetches OHLCV data via yfinance
│   ├── transform.py             # Cleans data, computes metrics, loads to SQLite
│   ├── analyze.py               # SQL queries for insights and summaries
│   └── run_pipeline.py          # Master script — runs all stages in order
├── database/
│   └── stocks.db                # SQLite database (4 tables)
├── csv_files/
│   ├── latest_prices.csv        # Most recent price per stock
│   ├── stock_summary.csv        # Avg metrics per stock
│   └── best_worst_days.csv      # Peak and lowest price days
├── dashboard/
│   └── app.py                   # Streamlit + Plotly dashboard
├── logs/
│   └── pipeline.log             # Timestamped run history
├── run_pipeline.bat             # Windows automation script
└── requirements.txt
```

---

## Database Design

The pipeline uses two normalized SQLite tables:

### `stock_prices` — raw daily OHLCV data
```
id              INTEGER   Primary key, auto-generated
ticker          TEXT      Stock ticker symbol
trade_date      TEXT      Trading date
open_price      REAL      Opening price
high_price      REAL      Daily high
low_price       REAL      Daily low
close_price     REAL      Closing price
volume          INTEGER   Shares traded
```

### `stock_analytics` — computed financial metrics
```
ticker          TEXT      Stock ticker symbol
trade_date      TEXT      Trading date
close_price     REAL      Closing price
open_price      REAL      Open price
volume          INTEGER   Cumulative volume
daily_return    REAL      Daily percentage return
trading_value   REAL      Close price × volume
moving_avg_7    REAL      7-day moving average
moving_avg_30   REAL      30-day moving average
volatility_7    REAL      7-day rolling volatility
```

### `aggregate_table` — reference table
```
ticker          TEXT      Primary key
avg_close       REAL      Average close price
avg_open        REAL      Average open price
avg_high        REAL      Average high price
avg_low         REAL      Average low price
max_close       REAL      Max close price
max_open        REAL      Max open price
currency        TEXT      PHP or USD
```

### `stocks` — reference table
```
ticker          TEXT      Primary key
name            TEXT      Full company name
market          TEXT      PSE or OTC
sector          TEXT      Industry sector
currency        TEXT      PHP or USD
```

---

## Pipeline Stages

```
Extract → Transform → Load → Analyze → Visualize
```

| Stage | Script | Description |
|---|---|---|
| Extract | extract_stocks.py | Fetches OHLCV data from Yahoo Finance via yfinance |
| Transform | transform.py | Cleans data, computes 8 financial metrics |
| Load | transform.py | Inserts clean data into SQLite via to_sql() |
| Analyze | analyze.py | SQL queries — latest prices, summaries, best/worst days |
| Visualize | dashboard/app.py | Interactive Streamlit + Plotly dashboard |

---

## Computed Financial Metrics

| Metric | Description |
|---|---|
| Daily return | Percentage change in closing price day over day |
| Trading value | Close price × volume — measures money flow |
| 7-day moving average | Short-term price trend indicator |
| 30-day moving average | Long-term price trend indicator |
| Volatility (7-day) | Rolling standard deviation of daily returns |
| Average OHLC | Mean open, high, low, close over the period |
| Max close and open | Peak closing and opening prices |
| Total volume | Cumulative shares traded over the period |

---

## Dashboard Sections

### Per-stock view (use dropdown to switch stocks)
- **KPI cards** — current price, daily return, 7-day MA, 30-day MA, volume, volatility
- **Candlestick chart** — full OHLC price history
- **Volume chart** — daily trading volume bar chart
- **Daily return chart** — day-by-day percentage return line chart

### Stocks comparison view
- **Close price comparison** — all three stocks on one line chart
- **Volatility comparison** — risk profile of each stock over time

### Summary section
- **Average OHLC by stock** — grouped bar chart
- **Summary table** — avg close, avg return, avg volatility per stock with company names via SQL JOIN

---

## SQL Queries Used

```sql
-- Latest price per stock
SELECT ticker, date, close
FROM stock_prices
ORDER BY date DESC LIMIT 3

-- Average metrics per stock
SELECT ticker,
       ROUND(AVG(close), 2) as avg_close,
       ROUND(AVG(daily_return), 4) as avg_return,
       ROUND(AVG(volatility), 4) as avg_volatility
FROM stock_metrics
GROUP BY ticker

-- JOIN company names to metrics
SELECT s.name, m.ticker, m.date, m.moving_avg_7, m.moving_avg_30
FROM stock_metrics m
JOIN stocks s ON m.ticker = s.ticker
ORDER BY m.date DESC

-- Most volatile periods
SELECT ticker,
       ROUND(AVG(volatility), 4) as avg_volatility,
       ROUND(MAX(volatility), 4) as peak_volatility
FROM stock_metrics
GROUP BY ticker
ORDER BY avg_volatility DESC
```

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/stock-pipeline.git
cd stock-pipeline
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the full pipeline

```bash
python scripts/run_pipeline.py
```

This will fetch stock data, compute all metrics, load into SQLite, and generate summary CSVs.

### 5. Launch the dashboard

```bash
streamlit run dashboard/app.py
```

---

## Automation

The pipeline is scheduled to run daily using **Windows Task Scheduler** via `run_pipeline.bat`. Each run fetches the latest stock data, updates the SQLite database, and refreshes all summaries automatically.

---

## Requirements

```
pandas
yfinance
streamlit
plotly
```

Install all with:

```bash
pip install -r requirements.txt
```

---

## Key Concepts Learned

- ETL pipeline design and implementation
- Relational database design with normalization
- SQLite database creation and management with sqlite3
- Writing SQL queries — SELECT, GROUP BY, JOIN, subqueries
- Financial metric computation — moving averages, volatility, daily returns
- Interactive dashboard development with Streamlit and Plotly
- Candlestick chart visualization for financial data
- Working with yfinance for market data ingestion
- Windows Task Scheduler automation

---

## License

This project is open source and available under the [MIT License](LICENSE).
