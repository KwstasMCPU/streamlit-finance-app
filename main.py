import streamlit as st
import os
import numpy as np
import pandas as pd
import requests

st.title("Currency rates")
st.write("""
## Currencies from all over the world
""")

url = 'http://data.fixer.io/api/'
ACCESS_KEY = os.environ.get('FIXER_API_KEY') 

# https://data.fixer.io/api/timeseries
#     ? access_key = API_KEY
#     & start_date = 2012-05-01
#     & end_date = 2012-05-25

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
        rates = rates.drop(columns=['success', 'timestamp'])
        rates = rates.rename(columns={'date':'Date', 'rates':'Rate'})
    except KeyError:
        print('Pass a valid date (YYYY-MM-DD)')
    except UnboundLocalError:
        print('historical date from 1999-01-01')
    return rates.loc[['USD','GBP','CHF','DKK','JPY','SGD']]

st.write(make_request(url, TYPE='latest'))