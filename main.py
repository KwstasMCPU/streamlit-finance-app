import streamlit as st
import yfinance as yf
import os
import numpy as np
import pandas as pd
import requests
from datetime import datetime

todays_date = datetime.today().strftime('%Y-%m-%d')
st.write(todays_date)

url = 'http://data.fixer.io/api/'
ACCESS_KEY = os.environ.get('FIXER_API_KEY') 


st.title("Finance App")
st.write("""
## Top Stocks and Currencies from all over the world
""")

st.sidebar.header('User Input Parameters')
st.sidebar.write('Stocks')
stock_ticker = st.sidebar.selectbox("Select stock", ("KO","TSLA","HPE","AMAT"))


def user_input():
    start_date = st.sidebar.slider('Start Date', datetime(2015, 1, 1), datetime(2021, 1, 1), value = datetime(2018, 1, 1))
    final_date = st.sidebar.slider('Final Date', datetime(2015, 1, 1), datetime(2021, 1, 15), value = datetime(2021, 1, 1))
    start_date = start_date.strftime('%Y-%m-%d')
    final_date = final_date.strftime('%Y-%m-%d')
    # start_date = st.sidebar.slider('Start Date', 0, 100, 50)
    # final_date = st.sidebar.slider('Final Date', 0, 100, 50)
    inputs = [start_date, final_date]
    return inputs

df = user_input()

tickerData = yf.Ticker(stock_ticker)
tickerDf = tickerData.history(period='1d', start=df[0] , end=df[1])
st.write(f"**{stock_ticker} - Close**")
st.write(f"From: {df[0]}  To: {df[1]}")
st.line_chart(tickerDf.Close)
st.write(f"**{stock_ticker} - Open**")
st.line_chart(tickerDf.Volume)





def make_request(url):
    '''
    Makes request to the fixer.io/api.
    the TYPE variable defines if a latest or a historic currency rate will be requested
    '''
    #data = {}
    try:
        url_request = ''.join([url, 'latest', '?access_key=', ACCESS_KEY])
        # measuring time in order to make a requests every 10 secs (since i am using the free key, i have limited amount of requests)
        data = requests.get(url_request).json()
        rates = pd.DataFrame(data)
        rates = rates.drop(columns=['success', 'base','timestamp'])
        rates = rates.rename(columns={'date':'Date', 'rates':'Rate'})
    except KeyError:
        print('Pass a valid date (YYYY-MM-DD)')
    except UnboundLocalError:
        print('historical date from 1999-01-01')
    return rates.loc[['USD','GBP','CHF','DKK','JPY','SGD']]

st.write("**Major currencies (EURO BASE)**")
st.write(make_request(url))








