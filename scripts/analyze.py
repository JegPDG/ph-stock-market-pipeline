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
    """, conn)

# Which days had the most money moving?





# print(agregate_table)
# print(h_mvng_30_avg)
# print(highest_volatility)
print(compare_daily_return)

conn.close()