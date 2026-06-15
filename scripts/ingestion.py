import pandas as pd
import yfinance as yf
import sqlite3
import os

# BDOUY, JBFCY, SM
tickers = ["BDOUY", "JBFCY", "SM"]

df = yf.download(tickers, period="1mo", interval="1d")

df_long = df.stack( level=1, future_stack=True).reset_index()

df_long = df_long.rename(
    columns={
        "Date": "trade_date",
        "Ticker": "ticker",
        "Open": "open_price",
        "High": "high_price",
        "Low": "low_price",
        "Close": "close_price",
        "Volume": "volume"
    }
)

df_long.columns.name = None 

conn = sqlite3.connect("sql_db/stocks.db")
cursor = conn.cursor()

df_long.to_sql(
  "stocks_prices", 
  conn, 
  if_exists="replace", #but use 'appened' later on, only use 'replace for the meantime
  index=False
  )

cursor.execute("PRAGMA table_info(stocks_prices)")

columns = cursor.fetchall()

for col in columns:
    # col[1] is the column name, col[2] is the data type
    print(f"Column: {col[1]} | Type: {col[2]}")


# Create a reference table for the tickers 


# df_from_db = pd.read_sql(f"SELECT * FROM stocks_prices", conn)
# print(df_from_db)

conn.close()








