import yfinance as yf
import pandas as pd
import numpy as np
import datetime as dt

tickers = 'TCS.NS'
start = dt.date.today() - dt.timedelta(365*2)
end = dt.date.today()

ohlcv = yf.download(tickers, start, end, interval = '1d')

def obv(df):
    df['direction'] = np.where(df['Adj Close']>= df['Adj Close'].shift(1), 1, -1)
    df.loc[df.index[0], 'direction'] = 0
    df['adj_vol'] = df['direction']*df['Volume']
    df['obv'] = (df['adj_vol'].cumsum())/100
    return df['obv']

obv(ohlcv).plot()