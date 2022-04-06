import yfinance as yf
import pandas as pd
import datetime as dt

tickers = 'TCS.NS'
start = dt.date.today() - dt.timedelta(365*2)
end = dt.date.today()

ohlcv = yf.download(tickers, start, end, interval = '1d')

def bollinger_band(df, n = 20, risk_multiple = 2, BB_range = False):
    df['ma'] = df['Close'].rolling(n).mean()
    df['BB_up'] = df['ma'] + risk_multiple * df['ma'].rolling(n).std()
    df['BB_dn'] = df['ma'] - risk_multiple * df['ma'].rolling(n).std()
    df['BB_range'] = df['BB_up']-df['BB_dn']
    df.dropna(inplace = True)
    if BB_range == True:
        return df.iloc[:,[-4,-3,-2, -1]]
    else:
        return df.iloc[:,[-4,-3,-2]]


bollinger_band(ohlcv, 20, 2).plot()


