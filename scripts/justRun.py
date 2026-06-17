import sqlite3

conn = sqlite3.connect("sql_db/stocks.db")
cursor = conn.cursor()

cursor.execute("DROP TABLE IF EXISTS agregate_table;")

conn.commit()
conn.close()