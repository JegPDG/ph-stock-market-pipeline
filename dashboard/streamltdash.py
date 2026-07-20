import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Retrive data from sql
@st.cache_data
def load_dashboard_data():
  with sqlite3.connect("sql_db/stocks.db") as conn:
    df_ag_tbl = pd.read_sql_query("SELECT ticker, avg_close, avg_high, avg_low, avg_open  FROM agregate_table", conn)
  
  with sqlite3.connect("sql_db/stocks.db") as conn:
    df_stck_anly = pd.read_sql_query("SELECT * FROM stocks_analytics", conn)
    df_stck_anly['trade_date'] = pd.to_datetime(df_stck_anly['trade_date']) # transform into datetime format
    df_stck_anly = df_stck_anly.sort_values(by='trade_date', ascending=True) # sort ASC
    df_stck_anly['trade_date'] = df_stck_anly['trade_date'].dt.strftime('%b %d') # Format to Month dd

  with sqlite3.connect("sql_db/stocks.db") as conn:
    df_stck_prc = pd.read_sql_query("SELECT * FROM stocks_prices", conn)
    df_stck_prc['trade_date'] = pd.to_datetime(df_stck_prc['trade_date'])
    df_stck_prc['trade_date'] = df_stck_prc['trade_date'].dt.strftime('%b %d')
  
  return df_ag_tbl, df_stck_anly, df_stck_prc

df_ag_tbl, df_stck_anly, df_stck_prc = load_dashboard_data()

# Rename columns
df_ag_tbl = df_ag_tbl.rename(columns={
  'avg_close':'Average Close',
  'avg_high':'Average High',
  'avg_low':'Average Low',
  'avg_open':'Average Open',
})

# ------------------------------------------------------------------------------------

st.set_page_config(layout="wide")

st.title("Stock Market Analytics Dashboard")

col1, col2, col3 = st.columns([1,2,1])


with col1:
  # Ticker Dropdown
  ticker = st.selectbox(
      "Select Stock",
      df_stck_prc["ticker"].unique()
  )

  with st.container(border=True):
        st.markdown(
          f"""
          <div style="font-size: 24px;">
              KPI of {ticker}
          </div>
          <div style="display: grid; grid-template-columns: 1fr 50px; font-size: 14px; padding: 0 20px 0px 20px;">
              <div> Current Price </div> 
              <div> 1 peos </div> 
              
          </div>

          <div style="font-size: 24px;">
          </div>
          """, 
          unsafe_allow_html=True
      )

# /////////////////////////////////////////


with col2:

  # Filter through ticker 
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

vol_bar = px.bar(
    stock_df,
    x="trade_date",
    y="volume",
    title="Volume Bar Chart",
    text_auto=True,  # Displays values on top of bars
)

st.plotly_chart(vol_bar, use_container_width=True)

# ------------------------------------------------------------------------------------


ticker_dly_rtn = df_stck_anly[df_stck_anly["ticker"] == ticker]
# Daily Return Line Chart per Ticker

dly_line = px.line(
  ticker_dly_rtn,
  x='trade_date',
  y='daily_return',
  title="Daily Return Line Chart"
)

st.plotly_chart(dly_line, use_container_width=True)

# ////////////////////////////////////////

# Line chart for Close Price

cls_line = px.line(
  df_stck_anly,
  x= "trade_date",
  y= "close_price",
  color="ticker"
)

st.plotly_chart(cls_line, use_container_width=True)

# Line chart for Volume 
vlm_line = px.line(
  df_stck_anly,
  x= "trade_date",
  y= "volume",
  color="ticker"
)

st.plotly_chart(vlm_line, use_container_width=True)


# Line chart for Volatility 
vlty_line = px.line(
  df_stck_anly,
  x= "trade_date",
  y= "volatility_7d",
  color="ticker"
)

st.plotly_chart(vlty_line, use_container_width=True)




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
