
# Goal is to create a 
# 1. Daily return field
# 2. Trading Value
# 3. Moving Average of 7 Days and Monthly
# 4. Volatility 

import sqlite3
import pandas as pd

conn = sqlite3.connect("sql_db/stocks.db")
cursor = conn.cursor()


df = pd.read_sql_query("SELECT * FROM stocks_prices", conn)

# ==========================================
#       SECTION 1
# ==========================================
# Aggregate Summary

# Create a table for the aggregate table
cursor.execute("""
  CREATE TABLE IF NOT EXISTS agregate_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL UNIQUE,
    avg_close REAL,
    avg_high REAL,
    avg_low REAL,
    avg_open REAL,
    max_close REAL,
    max_open REAL,
    total_volume INTEGER
  );
""")

# Get the data from the stock_prices table
query_1 = """
  SELECT  
      ticker,
      AVG(close_price) AS avg_close,
      AVG(high_price) AS avg_high,
      AVG(low_price) AS avg_low,
      AVG(open_price) AS avg_open,
      MAX(close_price) as max_close,
      MAX(open_price) as max_open,
      SUM(volume) as total_volume
  FROM stocks_prices
  GROUP BY ticker
"""
agregate_df = pd.read_sql_query(query_1, conn)

agregate_tuples = list(agregate_df.itertuples(index=False, name=None))

cursor.executemany("""
  INSERT OR IGNORE INTO agregate_table
  (ticker, avg_close, avg_high, avg_low, avg_open, max_close, max_open, total_volume)
  VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", agregate_tuples)


# ==========================================
#       SECTION 2
# ==========================================
# 1. Daily return field
# 2. Trading Value
# 3. Moving Average of 7 Days and Monthly

query_for_ticker_1 = """
  SELECT 
    trade_date,
    ticker,
    close_price,
    open_price,
    volume,
    (close_price - LAG(close_price) OVER(PARTITION BY ticker ORDER BY trade_date)) / 100 AS daily_return,
    (close_price * volume) AS trading_value,

    AVG(close_price) OVER(
      PARTITION BY ticker 
      ORDER BY trade_date
      ROWS BETWEEN 6 PRECEDING AND CURRENT ROW
      ) as moving_avg_7d,

    AVG(close_price) OVER( 
      PARTITION BY ticker
      ORDER BY trade_date
      ROWS BETWEEN 29 PRECEDING AND CURRENT ROW
    ) as moving_avg_30d

  FROM stocks_prices

"""
metrics_df = pd.read_sql_query(query_for_ticker_1, conn)

# Create the volatility
metrics_df['volatility_7d'] = metrics_df.groupby('ticker')['daily_return'].transform(
    lambda x: x.rolling(window=7).std()
)

# Get unique tickers dynamically from the database
cursor.execute("SELECT DISTINCT ticker FROM stocks_prices;")
unique_tickers = [row[0] for row in cursor.fetchall()]

print(f"\n--- Processing analytical loops for tickers: {unique_tickers} ---")

# Loop optimization example if you need to isolate or inspect per-ticker dataframes
for ticker in unique_tickers:
    ticker_df = metrics_df[metrics_df['ticker'] == ticker].sort_values('trade_date')
    print(f"\nTicker: {ticker} | Total Records: {len(ticker_df)}")
    print(ticker_df[['trade_date', 'daily_return', 'trading_value', 'moving_avg_7d', 'volatility_7d']].tail(3))

metrics_df.to_sql(
    "stocks_analytics", 
    conn, 
    if_exists="replace", 
    index=False
)


print(metrics_df)
# print(agregate_df.info())
# print(df)
conn.commit()
conn.close()