import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt

tickers = 'ITC.NS'
start = dt.date.today() - dt.timedelta(365*2)
end = dt.date.today()

ohlcv = yf.download(tickers, start, end, interval = '1d')

df = ohlcv.copy()


def stochastics(df, n = 14, d = False):
    df['close'] = df['Close']
    df['k'] = pd.Series(dtype = object)
    for i in list(range(n,len(df))):
        df.iloc[i, -1] = (df.iloc[i, -2]-df.iloc[i-n:i+1, -2].min()) / (df.iloc[i-n:i+1, -2].max() - df.iloc[i-n:i+1, -2].min())
    df['%k'] = df['k'].rolling(3).mean()
    df['%D'] = df['%k'].rolling(3).mean()
    df.dropna(inplace = True)
    if d == False:
        return df.iloc[:,-2]
    else:
        return df.iloc[:, -1]

stochastics(df, d = False).plot()