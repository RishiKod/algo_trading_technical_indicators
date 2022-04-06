import yfinance as yf
import pandas as pd
import datetime as dt

tickers = 'INFY.NS'
start = dt.date.today() - dt.timedelta(365*5)
end = dt.date.today()

ohlcv = yf.download(tickers, start, end, interval = '1d')


def atr(df, n = 20):
    df= ohlcv.copy()
    df['h-l'] = abs(df["High"] - df["Low"])
    df['h-pc'] = abs(df['High'] - df['Close'].shift(1))
    df['l-pc'] = abs(df['Low'] - df['Close'].shift(1))
    df['tr'] = df[['h-l', 'h-pc', 'l-pc']].max(axis = 1, skipna = False)
    df['atr'] = df['tr'].rolling(n).mean()
    df.drop(['h-l', 'h-pc', 'l-pc'], axis = 1, inplace = True)
    df.dropna(inplace = True)
    return df['atr']


atr(ohlcv, 20).plot()