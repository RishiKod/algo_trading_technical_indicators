import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt

tickers = 'ITC.NS'
#start = dt.date.today() - dt.timedelta(100)
#end = dt.date.today()
start = '2014-12-31'
end = dt.date.today()

ohlcv = yf.download(tickers, start, end, interval = '1d')

def stochastic_rsi(df, n = 14):
    df.dropna(inplace = True)
    df['gain'] = np.where(df['Close']>df['Close'].shift(1), df['Close']-df['Close'].shift(1), 0)
    df['loss'] = np.where(df['Close']<df['Close'].shift(1), abs(df['Close'].shift(1)-df['Close']), 0)
    df.drop(df.index[0], inplace = True)
    df['avg_gain'] = pd.Series(dtype = object)
    df.iloc[n-1, -1] = df.iloc[:n, -3].mean()
    df['avg_loss'] = pd.Series(dtype = object)
    df.iloc[n-1, -1] = df.iloc[:n, -3].mean()
    for i in list(range(n,len(df))):
        df.iloc[i, -2] = ((df.iloc[i-1, -2]*13)+df.iloc[i, -4])/n
        df.iloc[i, -1] = ((df.iloc[i-1, -1]*13)+df.iloc[i, -3])/n
    df['RS'] = df['avg_gain']/df['avg_loss']
    df['RSI'] = 100 - (100/(1+df['RS']))
    df['stochastic_RSI'] = pd.Series(dtype = object)
    for i in list(range((n-1)*2,len(df))):
        df.iloc[i, -1] = (df.iloc[i, -2]-df.iloc[i-n:i+1, -2].min()) / (df.iloc[i-n:i+1, -2].max() - df.iloc[i-n:i+1, -2].min())
    return df['stochastic_RSI']


stochastic_rsi(ohlcv,14).plot()