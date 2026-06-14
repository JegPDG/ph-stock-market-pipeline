
# Goal is to create a 
# 1. Daily return field
# 2. Trading Value
# 3. Moving Average of 7 Days and Monthly
# 4. Volatility 

import sqlite3
import pandas as pd

conn = sqlite3.connect("sql_db/stocks.db")

df = pd.read_sql_query("SELECT * FROM stocks_prices", conn)

# Agregation Query
query_1 = """
  SELECT  
      ticker,
      AVG(close_price) AS avg_close,
      AVG(high_price) AS avg_high,
      AVG(low_price) AS avg_low,
      AVG(open_price) AS avg_open,
      MAX(close_price) as max_close,
      MAX(open_price) as max_close,
      SUM(volume) as total_volume
  FROM stocks_prices
  GROUP BY ticker
"""
agregate_df = pd.read_sql_query(query_1, conn)



print(agregate_df)
# print(df)

conn.close()