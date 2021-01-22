import streamlit as st
import yfinance as yf
import os
import numpy as np
import pandas as pd
import requests
from datetime import datetime

todays_date = datetime.today().strftime('%Y-%m-%d')

url = 'http://data.fixer.io/api/'
ACCESS_KEY = os.environ.get('FIXER_API_KEY') 

def make_request(url, base = 'EUR'):
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

def get_stock_data(inputs):
    tickerData = yf.Ticker(stock_ticker)
    tickerDf = tickerData.history(period='1d', start=inputs[0] , end=inputs[1])
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
stock_ticker = st.sidebar.selectbox("Select stock", ("KO","TSLA","HPE","AMAT"))

currency_base = st.sidebar.radio('Currency Base', ('EUR','USD','GBP','DKK'))

start_date = st.sidebar.slider('Start Date', datetime(2015, 1, 1), datetime(2021, 1, 1), value = datetime(2018, 1, 1))
final_date = st.sidebar.slider('Final Date', datetime(2015, 1, 1), datetime(2021, 1, 15), value = datetime(2021, 1, 1))
start_date = start_date.strftime('%Y-%m-%d')
final_date = final_date.strftime('%Y-%m-%d')
inputs = [start_date, final_date]

st.write(f"**Major currencies ({currency_base})**")
st.write(make_request(url, currency_base))
tickerDf = get_stock_data(inputs)
st.write(f"**{stock_ticker} - Close**")
st.write(f"From: {inputs[0]}  To: {inputs[1]}")
st.line_chart(tickerDf.Close)
st.write(f"**{stock_ticker} - Volume**")
st.line_chart(tickerDf.Volume)




