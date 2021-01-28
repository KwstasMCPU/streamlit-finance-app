import streamlit as st
import yfinance as yf
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import requests
from datetime import datetime, timedelta

todays_date = datetime.today().strftime('%Y-%m-%d')

url = 'http://data.fixer.io/api/'
ACCESS_KEY = os.environ.get('FIXER_API_KEY') 

def make_request(base = 'EUR'):
    '''
    Makes request to the fixer.io/api.
    the TYPE variable defines if a latest or a historic currency rate will be requested
    '''
    url_request = ''.join([url, 'latest', '?access_key=', ACCESS_KEY])
    data = requests.get(url_request).json()
    rates = pd.DataFrame(data)
    rates = rates.drop(columns=['success', 'base','timestamp'])
    rates = rates.rename(columns={'date':'Date', 'rates':'Rate'})
    major_rates_base_EUR = rates.loc[['USD','GBP','DKK','CHF','JPY','AUD','CAD']]
    if base != 'EUR':
        major_rates_in_other_base = change_base(major_rates_base_EUR, base)
        return major_rates_in_other_base
    return major_rates_base_EUR

def change_base(rates_df, base):
    '''
    This functions calculates the exchange rates for BASE other than EUR.
    (There is no option to request to the API with different BASE on the free plan.)
    Uses the cross exchange formula for the calculation. Also adds the BASE/EUR rate
    to the returned dataframe.

    Parameters:
        rates_df (pandas DataFrame): The DataFrame contaning the rates, obtained by the make_request().
        base (str): The Base currency the user wish to switch to. The first currency that appears in the pair quotation.

    Returns:
        rates_df (pandas DataFrame): The converted DataFrame with the rates converted to the new BASE currency. Also, the
        BASE/EUR rate is calculated and added in the same index as the BASE/BASE would had been.
    '''
    base_cur = rates_df.Rate.loc[base]
    rates_df.Rate = rates_df.Rate / base_cur
    BASE_to_EUR_rate = 1.0 / base_cur
    d = rates_df.Date.loc[base]
    rates_df.rename(index={base:'EUR'}, inplace = True)
    rates_df.loc['EUR'] = [d, BASE_to_EUR_rate]
    return rates_df

def get_stock_data(input):
    tickerData = yf.Ticker(stock_ticker)
    interval = '1m'
    if input == '5d' or input == '1wk':
        interval = '15m'
    if input == '1mo' or input == '3mo':
        interval = '1d'
    if input == 'max':
        interval = '5d'
    tickerDf = tickerData.history(period=input, interval=interval, prepost=True)
    return tickerDf

### WEB APP ###

## UPPER ##
st.write(todays_date)
st.title("Finance App")
st.write("""
## Top Stocks and Currencies from all over the world
""")

## SIDE BAR ##
st.sidebar.header('User Input Parameters')
st.sidebar.write('Stocks')

    # user inputs #
stock_ticker = st.sidebar.selectbox("Select stock", ("KO","TSLA","HPE","AMAT","GME"))
input = st.sidebar.radio('Period', ("1d","5d","1wk","1mo","3mo","max"))

currency_base = st.sidebar.radio('Currency Base', ('EUR','USD','GBP','DKK','JPY'))

st.write(f"**Major currencies ({currency_base})**")
st.write(make_request(currency_base))
tickerDf = get_stock_data(input)
st.write(f"**{stock_ticker} - Close**")
fig1, ax1 = plt.subplots()
ax1.plot(tickerDf.index.values, tickerDf['Close'])
st.pyplot(fig1)

st.write(f"**{stock_ticker} - Volume**")
fig2, ax2 = plt.subplots()
ax2.plot(tickerDf.index.values, tickerDf['Volume'])
st.pyplot(fig2)





