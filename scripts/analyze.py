import sqlite3
import pandas as pd

conn = sqlite3.connect("sql_db/stocks.db")
cursor = conn.cursor()

# df = pd.read_sql_query("SELECT * FROM stocks_prices", conn)

agregate_table = pd.read_sql_query("SELECT * FROM agregate_table", conn)

# -- Which stock has the highest 30-day moving average right now?
h_mvng_30_avg = pd.read_sql_query("""
    SELECT  
      ticker,
      moving_avg_30d,
      trade_date,                            
      RANK() OVER (ORDER BY moving_avg_30d DESC) as avg_30d_rank
    FROM stocks_analytics                             
    """, conn)

# -- Which day had the highest volatility per stock?
highest_volatility = pd.read_sql_query("""
    SELECT 
      *,
      RANK() OVER (PARTITION BY ticker ORDER BY volatility_7d DESC) as h_vol_avg
    FROM (SELECT  
      ticker,
      volatility_7d,
      trade_date                         
    FROM stocks_analytics
    WHERE volatility_7d IS NOT NULL)                                                           
    """, conn)

# -- Compare average daily return per stock
compare_daily_return = pd.read_sql_query("""
   SELECT 
      trade_date,
      ticker,
      daily_return
    FROM stocks_analytics
    WHERE daily_return IS NOT NULL
    """, conn)

# Which days had the most money moving?
act_trad_d = pd.read_sql_query("""
   SELECT 
      ticker,
      trade_date,
      volume,
      trading_value
    FROM stocks_analytics
    ORDER By trading_value DESC                           
    """, conn)



# Save all in different CSV for dashboard 
# create a for loop for this
dataFrames = [
    (agregate_table, "aggregate_tbl"), 
    (h_mvng_30_avg, "h_moving_30d_avg"),
    (highest_volatility, "highest_volatility"),
    (compare_daily_return, "compare_daily_return"),
    (act_trad_d, "act_trad_d")
    ]

for dataframe, path in dataFrames:
  dataframe = dataframe.reset_index()

  dataframe.to_csv(f"sql_db/csv_files/{path}.csv", index=False)
  print("Done saving:", path)

# print(agregate_table.head())
# print(h_mvng_30_avg.head())
# print(highest_volatility.head())
# print(compare_daily_return.head())
# print(act_trad_d.head())

conn.commit()
conn.close()