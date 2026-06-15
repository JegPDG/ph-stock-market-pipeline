
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

# Agregation Query

# Create a table for the aggregate table
cursor.execute("""
  CREATE TABLE IF NOT EXISTS agregate_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticker TEXT NOT NULL,
    avg_close REAL,
    avg_high REAL,
    avg_low REAL,
    avg_open REAL,
    max_close REAL,
    max_open REAL,
    total_volume INTEGER
  );
""")

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

# Save to sqlite DB 
# Uncomment when finished !!
# agregate_df.to_sql(
#   "agregate_table", 
#   conn, 
#   if_exists="replace",
#   index=False
# )

# Create 3 data frames for each ticker
# then use the lag func in SQL to create a daily return
# Combine the three data frame and sort by Date

# Create a reference table for the tickers
# Optimize the code to (use for loops)

frame_1 = []

query_for_ticker_1 = """
  SELECT *
  FROM stocks_prices
  WHERE ticker == "BDOUY"
"""

frame_1 = pd.read_sql_query(query_for_ticker_1, conn)


print(frame_1)






# print(agregate_df)
# print(df)

conn.close()