import streamlit as st
import yfinance as yf
import os
import numpy as np
import pandas as pd
import requests


from datetime import datetime, timedelta

url = 'http://data.fixer.io/api/'
ACCESS_KEY = os.environ.get('FIXER_API_KEY') 


st.sidebar.header('User Input Parameters')
st.sidebar.write('Stocks')

def stock_time_series_user_input():
    # start_date = st.sidebar.slider('Start Date', value = datetime.today() - timedelta(365))
    # final_date = st.sidebar.slider('Final Date', value = datetime.today())
    start_date = st.sidebar.slider('Start Date', min_value= datetime(2015, 1, 1), max_value=datetime.today(), value = datetime.today() - timedelta(365))
    final_date = st.sidebar.slider('Final Date', min_value= datetime(2015, 1, 1), max_value=datetime.today(), value = datetime.today())
    start_date = start_date.strftime('%Y-%m-%d')
    final_date = final_date.strftime('%Y-%m-%d')
    return [start_date, final_date]

start_end = stock_time_series_user_input()

def stock_time_series(start_end):
    tickerData = yf.Ticker('KO')
    tickerDf = tickerData.history(period='1d', start=start_end[0] , end=start_end[1])
    return tickerDf


def make_request(url, TYPE='latest'):
    '''
    Makes request to the fixer.io/api.
    the TYPE variable defines if a latest or a historic currency rate will be requested
    '''
    #data = {}
    try:
        url_request = ''.join([url, TYPE, '?access_key=', ACCESS_KEY])
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


st.title("Finance App")
st.write("""
## Top Stocks and Currencies from all over the world
""")




st.write("**Major currencies (EURO BASE)**")
st.write(make_request(url, TYPE='latest'))

df = stock_time_series(start_end)
st.write("**Coca-cola stock (KO) - Close**")
st.line_chart(df.Close)
st.write("**Coca-cola stock (KO) - Open**")
st.line_chart(df.Volume)