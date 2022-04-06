import pandas as pd
import yfinance as yf
import numpy as np
import datetime as dt

tickers = 'TCS.NS'
#start = dt.date.today() - dt.timedelta(365)
#end = dt.date.today()
start = '2014-12-31'
end = dt.date.today()

ohlcv = yf.download(tickers, start, end, interval = '1d')

def renko(df, atr_n = 20):   
    df['h-l'] = abs(df["High"] - df["Low"])
    df['h-pc'] = abs(df['High'] - df['Close'].shift(1))
    df['l-pc'] = abs(df['Low'] - df['Close'].shift(1))
    df['tr'] = df[['h-l', 'h-pc', 'l-pc']].max(axis = 1, skipna = False)
    df['atr'] = df['tr'].rolling(atr_n).mean()
    df.drop(['h-l', 'h-pc', 'l-pc'], axis = 1, inplace = True)
    df.dropna(inplace = True)
    df['renko'] = pd.Series(dtype = object)
    base = df.loc[df.index[0], 'Close']
    for i in list(range(len(df))):
        if df.loc[df.index[i],'Close'] > base + df.loc[df.index[i],'atr']:
            base = df.loc[df.index[i],'Close']
            df.loc[df.index[i],'renko'] = 1
        elif df.loc[df.index[i], 'Close'] < base - df.loc[df.index[i],'atr']:
            base = df.loc[df.index[i],'Close']
            df.loc[df.index[i],'renko'] = -1
        else:
            df.loc[df.index[i],'renko'] = 0
    return df['renko']

renko(ohlcv).plot()