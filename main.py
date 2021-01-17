import streamlit as st
import yfinance as yf
import os
import numpy as np
import pandas as pd
import requests


from datetime import datetime, timedelta

url = 'http://data.fixer.io/api/'
ACCESS_KEY = os.environ.get('FIXER_API_KEY') 


def stock_time_series(tickerSymbol, start = '2020-01-01' , end = datetime.today().strftime('%Y-%m-%d')):
    tickerData = yf.Ticker(tickerSymbol)
    tickerDf = tickerData.history(period='1d', start=start , end=end)
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
df = stock_time_series('KO', '2019-05-01')
st.write("**Coca-cola stock (KO) - Close**")
st.line_chart(df.Close)
st.write("**Coca-cola stock (KO) - Open**")
st.line_chart(df.Volume)

st.sidebar.header('User Input Parameters')
