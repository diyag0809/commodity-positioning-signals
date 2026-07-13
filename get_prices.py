import yfinance as pd_yf
import pandas as pd

corn_data = pd_yf.download('ZC=F', start='2006-01-01', end='2026-07-13')

price_data = pd.read_csv('data/price_data.csv', index_col='Date', parse_dates=True)
price_data['CORN - CHICAGO BOARD OF TRADE'] = corn_data['Close'].squeeze()

price_data.to_csv('data/price_data.csv')
print("Added corn data, new shape:")
print(price_data.shape)