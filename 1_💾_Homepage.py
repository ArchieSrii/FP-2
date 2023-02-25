#importing libraries

import streamlit as st
from datetime import datetime
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import yfinance as yf
from plotly import graph_objs as go 
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.filters.hp_filter import hpfilter 


sidebar_flag = None
sidebar_flag2 = None 
# Page title and config
st.set_page_config(
    page_title='Stock Forecasting'
)
st.title('Stock Forecasting')
# setting up structure to retrive data
ticker=""
ticker = st.sidebar.text_input('Ticker')
comp_list = []  # Create an empty list for the companies
a=1
comp_list
comp_list.append(ticker)
comp_list=list(comp_list.keys())

a=1
a
comp_list

# ticker2 = st.sidebar.text_input('Second Ticker (ideally broader market index)')
# stock_name2 = 'DJIA'
stock_name2=""
stock_name2 = st.sidebar.text_input('Ticker2')
comp_list.append(stock_name2) 

b=2
b
comp_list
#aded for checking
#comp_list




sidebar_flag = ticker 
sidebar_flag2  = stock_name2
if ticker and stock_name2 is not None:
    # Extracting data
    end = datetime.now()
    start = datetime(end.year - 1, end.month, end.day)

    for stock in comp_list:
        d=3
        d
        stock
        globals()[stock] = yf.download(stock, start, end)
    
    comp_list1= ['AAPL','DJIA']
    company_list = [eval(x) for x in comp_list1]
    e=5
    e
    company_list
    company_name = comp_list1
    f=6
    f
    company_name
    #["Company1", "DJIA"]
    

    for company, com_name in zip(company_list, company_name):
        company["company_name"] = com_name
    df = pd.concat(company_list, axis=0) 
    #checking df
    df
    df=df.reset_index()
    df["Date"] = pd.to_datetime(df["Date"], format='%Y-%m-%d').dt.date
    st.dataframe(df[df['company_name'] == ticker].tail(10))  
    st.subheader(f'{ticker} and {stock_name2} Data')
   

    # Stock Close Chart
    stock_close = df[df['company_name'] == ticker]
    def plot_ticker():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df.Date,y = stock_close['Close'],name = f'{ticker} Close'))
        fig.layout.update(title_text = f'{ticker} Latest Year Close',xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    plot_ticker() 

    # Index Close Chart
    index_close = df[df['company_name'] == stock_name2]
    def plot_index():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df.Date,y = index_close['Close'],name = f'{stock_name2} Close'))
        fig.layout.update(title_text = f'{stock_name2} Latest Year Close',xaxis_rangeslider_visible=True)
        st.plotly_chart(fig)
    plot_index()

    # Moving Averages Charts

    def ticker_ma():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df.Date,y = stock_close['Close'].rolling(10).mean(),name = f'{ticker} 10 day Moving Average'))
        fig.add_trace(go.Scatter(x = df.Date,y = stock_close['Close'].rolling(20).mean(),name = f'{ticker} 20 day Moving Average'))
        fig.add_trace(go.Scatter(x = df.Date,y = stock_close['Close'].rolling(50).mean(),name = f'{ticker} 50 day Moving Average'))
        fig.add_trace(go.Scatter(x = df.Date,y = stock_close['Close'],name = f'{ticker} Close'))
        fig.layout.update(title_text = f'{ticker} Moving Average',xaxis_rangeslider_visible=True)

        st.plotly_chart(fig)

    ticker_ma()

    def ticker2_ma():
        fig = go.Figure()
        fig.add_trace(go.Scatter(x = df.Date,y = index_close['Close'].rolling(10).mean(),name = f'{stock_name2} 10 day Moving Average'))
        fig.add_trace(go.Scatter(x = df.Date,y = index_close['Close'].rolling(20).mean(),name = f'{stock_name2} 20 day Moving Average'))
        fig.add_trace(go.Scatter(x = df.Date,y = index_close['Close'].rolling(50).mean(),name = f'{stock_name2} 50 day Moving Average'))
        fig.add_trace(go.Scatter(x = df.Date,y = index_close['Close'],name = f'{stock_name2} Close'))
        fig.layout.update(title_text = f'{stock_name2} Moving Average',xaxis_rangeslider_visible=True)

        st.plotly_chart(fig)

    ticker2_ma() 



    #extracting trend and cyclicity using hpfilter

    st.subheader(f'{ticker} Decomposition')
    data_cycle, data_trend = hpfilter(stock_close["Close"], lamb=1600)
    stock_close['trend'] = data_trend
    stock_close["cycle"] = data_cycle

    stock_close=stock_close.set_index('Date')
    stock_close.sort_index(inplace=True)
    stock_close.index.freq="D"

    def plot_decompose():
        decomp = seasonal_decompose(stock_close["Close"],period = int(len(stock_close)/6))  
        st.pyplot(decomp.plot()) 
    plot_decompose()

    #extracting trend and cyclicity using hpfilter

    st.subheader(f'{stock_name2} Decomposition')
    data_cycle, data_trend = hpfilter(index_close["Close"], lamb=1600)
    index_close['trend'] = data_trend
    stock_close["cycle"] = data_cycle

    index_close=index_close.set_index('Date')
    index_close.sort_index(inplace=True)
    index_close.index.freq="D"

    def plot_decompose():
        decomp = seasonal_decompose(index_close["Close"],period = int(len(index_close)/6))  
        st.pyplot(decomp.plot()) 
    plot_decompose()

else:
    st.write('Please input tickers') 

