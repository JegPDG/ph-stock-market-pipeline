import pandas as pd
import sqlite3

conn = sqlite3.connect("sql_db/stocks.db")

df_from_db = pd.read_sql(f"SELECT * FROM stocks_prices", conn)

pd.testing.assert_frame_equal(df_original, df_from_db)