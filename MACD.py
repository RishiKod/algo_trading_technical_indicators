import yfinance as yf
import pandas as pd
import datetime as dt

tickers = 'ITC.NS'
#start = dt.date.today() - dt.timedelta(365)
#end = dt.date.today()
start = '2014-12-31'
end = dt.date.today()

ohlcv = yf.download(tickers, start, end, interval = '1d')


def macd(df, fast = 12, slow = 26, signal = 9):
    df = df.copy()
    df['ma_fast'] = df['Close'].ewm(span = fast, min_periods = fast).mean()
    df['ma_slow'] = df['Close'].ewm(span = slow, min_periods = slow).mean()
    df['macd'] = df['ma_fast'] - df['ma_slow']
    df['signal'] = df['macd'].ewm(span = signal, min_periods = signal).mean()
    df.dropna(inplace = True)
    return df[['macd', 'signal']]

abc = pd.DataFrame()
abc = macd(ohlcv)


