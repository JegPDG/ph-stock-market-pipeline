import pandas as pd
import yfinance as yf
import sqlite3
import os

# BDOUY, JBFCY, SM
tickers = ["BDOUY", "JBFCY", "SM"]

# Stock reference
stocks_data = [
    ("SM.PS", "SM Investments Corporation", "PSE", "Conglomerates", "PHP"),
    ("JBFCY", "Jollibee Foods Corporation", "OTC", "Consumer Staples", "USD"),
    ("BDOUY", "BDO Unibank Inc", "OTC", "Financials", "USD")
]

# Downloading the tickers
df = yf.download(tickers, period="1mo", interval="1d")

# This makes it into a clean table
df_long = df.stack( level=1, future_stack=True).reset_index()

#  Renaming the columns
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

# Crate an db engine
conn = sqlite3.connect("sql_db/stocks.db")

cursor = conn.cursor()

# Saving to sql
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
# 1 Create the table
conn.execute("""
    CREATE TABLE IF NOT EXISTS stocks (
        ticker TEXT PRIMARY KEY,
        name TEXT,
        market TEXT,
        sector TEXT,
        currency TEXT
    )
""")

conn.executemany("""
    INSERT OR IGNORE INTO stocks (ticker, name, market, sector, currency)
    VALUES (?, ?, ?, ?, ?)
""", stocks_data)



print(df_long)
# df_from_db = pd.read_sql(f"SELECT * FROM stocks_prices", conn)
# print(df_from_db)
conn.commit()
conn.close()








