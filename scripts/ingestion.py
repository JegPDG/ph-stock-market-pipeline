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

df_long.to_sql(
  "stocks_prices", 
  conn, 
  if_exists="replace", #but use 'appened' later on, only use 'replace for the meantime
  index=False
  )

df_from_db = pd.read_sql(f"SELECT * FROM stocks_prices", conn)

pd.testing.assert_frame_equal(df_long, df_from_db)


conn.close()

print(df_long.columns)

print("Verification successful! The DataFrames match.")






