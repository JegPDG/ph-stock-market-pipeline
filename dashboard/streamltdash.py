import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

@st.cache_data
def load_dashboard_data():
  with sqlite3.connect("sql_db/stocks.db") as conn:
    df_ag_tbl = pd.read_sql_query("SELECT ticker, avg_close, avg_high, avg_low, avg_open  FROM agregate_table", conn)

  return df_ag_tbl

df_ag_tbl = load_dashboard_data()


# GROUPED BAR CHART 
st.header("Stock Summary")

df_long = df_ag_tbl.melt(
  id_vars="ticker",
  value_vars=['avg_close', 'avg_high', 'avg_low', 'avg_open'],
  var_name="Metric",
  value_name="Price"
)

fig = px.bar(
    df_long,
    x="ticker",
    y="Price",
    color="Metric",
    barmode="group",
    title="Average Stock Prices by Ticker",
    labels={
        "ticker": "Stock",
        "Price": "Price",
        "Metric": "Price Type"
    }
)

st.plotly_chart(fig, use_container_width=True)

print (df_ag_tbl.info())