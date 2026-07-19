import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Retrive daat from sql
@st.cache_data
def load_dashboard_data():
  with sqlite3.connect("sql_db/stocks.db") as conn:
    df_ag_tbl = pd.read_sql_query("SELECT ticker, avg_close, avg_high, avg_low, avg_open  FROM agregate_table", conn)
  
  with sqlite3.connect("sql_db/stocks.db") as conn:
    df_stck_anly = pd.read_sql_query("SELECT * FROM stocks_analytics", conn)
    # Format the date time to (Month 00)
    df_stck_anly['trade_date'] = pd.to_datetime(df_stck_anly['trade_date'])
    df_stck_anly = df_stck_anly.sort_values(by='trade_date')
    print(df_stck_anly)
    df_stck_anly['trade_date'] = df_stck_anly['trade_date'].dt.strftime('%b %d')

  with sqlite3.connect("sql_db/stocks.db") as conn:
    df_stck_prc = pd.read_sql_query("SELECT * FROM stocks_prices", conn)
    df_stck_prc['trade_date'] = pd.to_datetime(df_stck_prc['trade_date'])
    df_stck_prc['trade_date'] = df_stck_prc['trade_date'].dt.strftime('%b %d')
  
  return df_ag_tbl, df_stck_anly, df_stck_prc

df_ag_tbl, df_stck_anly, df_stck_prc = load_dashboard_data()
df_ag_tbl = df_ag_tbl.rename(columns={
  'avg_close':'Average Close',
  'avg_high':'Average High',
  'avg_low':'Average Low',
  'avg_open':'Average Open',

})

# Ticker Dropdown
ticker = st.selectbox(
    "Select Stock",
    df_stck_prc["ticker"].unique()
)


# # GROUPED BAR CHART 
# st.header("Stock Summary")

# # Group by Ticker
# df_long = df_ag_tbl.melt(
#   id_vars="ticker",
#   value_vars=['Average Close', 'Average High', 'Average Low', 'Average Open'],
#   var_name="Metric",
#   value_name="Price"
# )

# fig = px.bar(
#     df_long,
#     x="ticker",
#     y="Price",
#     color="Metric",
#     barmode="group",
#     title="Average Stock Prices by Ticker",
#     labels={
#         "ticker": "Stock",
#         "Price": "Price",
#         "Metric": "Price Type"
#     }
# )

# st.plotly_chart(fig, use_container_width=True)

# # Group by ticker
# fig1 = px.bar(
#     df_long,
#     x="Metric",
#     y="Price",
#     color="ticker",
#     barmode="group",
#     title="Average Stock Prices by Metric",
#     labels={
#         "ticker": "Stock",
#         "Price": "Price",
#         "Metric": "Price Type"
#     }
# )

# st.plotly_chart(fig1, use_container_width=True)


# /////////////////////////////////////////

st.header("Stock Candlestick Chart")

# filter through ticker 
stock_df = df_stck_prc[df_stck_prc["ticker"] == ticker]

fig2 = go.Figure(
    data=[
        go.Candlestick(
            x=stock_df["trade_date"],
            open=stock_df["open_price"],
            high=stock_df["high_price"],
            low=stock_df["low_price"],
            close=stock_df["close_price"]
        )
    ]
)

fig2.update_layout(
    title=f"{ticker} Candlestick Chart",
    xaxis_title="Date",
    yaxis_title="Price",
    xaxis_rangeslider_visible=False
)

st.plotly_chart(fig2, use_container_width=True)

# Volume Bar Chart per Ticker

st.header("Volume Chart")
st.bar_chart(
  stock_df,
  x="trade_date",
  y='volume'
)

ticker_dly_rtn = df_stck_anly[df_stck_anly["ticker"] == ticker]
# Daily Return Line Chart per Ticker
st.header("Daily Return")
st.line_chart(
  ticker_dly_rtn,
  x= "trade_date",
  y= "daily_return"
)




# ////////////////////////////////////////

# Line chart for Close Price
st.header("Close Price Comparison")
st.line_chart(
  df_stck_anly,
  x= "trade_date",
  y= "close_price",
  color="ticker"
)

# Line chart for Volume 
st.header("Volume Comparison")

st.line_chart(
  df_stck_anly,
  x= "trade_date",
  y= "volume",
  color="ticker"
)

# Line chart for Volatility 
st.header("Volatility Comparison")

st.line_chart(
  df_stck_anly,
  x= "trade_date",
  y= "volatility_7d",
  color="ticker"
)