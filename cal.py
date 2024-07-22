from datetime import timedelta
import pandas as pd
import numpy as np

df_5m = pd.read_csv('ethusdt_5m.csv')

df_5m['open_time'] = pd.to_datetime(df_5m['open_time'], unit='ms')
df_5m['close_time'] = pd.to_datetime(df_5m['close_time'], unit='ms')

df_5m = df_5m.sort_values(by='open_time')

data_10m = []

time_window = timedelta(minutes=10)

start_time = df_5m['open_time'].min()
end_time = df_5m['open_time'].max()

current_time = start_time

while current_time <= end_time:
    mask = (df_5m['open_time'] >= current_time) & (df_5m['open_time'] < current_time + time_window)
    subset = df_5m[mask]
    
    if not subset.empty:
        open_price = subset['open'].iloc[0]
        high_price = subset['high'].max()
        low_price = subset['low'].min()
        close_price = subset['close'].iloc[-1]
        close_time = subset['close_time'].iloc[-1]

        data_10m.append([current_time, open_price, high_price, low_price, close_price, close_time])
    
    current_time += time_window

df_10m = pd.DataFrame(data_10m, columns=['open_time', 'open', 'high', 'low', 'close', 'close_time'])


print(df_10m)

df_10m = df_10m.dropna()  # remove NaN value
df_10m = pd.DataFrame(df_10m)  # Convert to DataFrame
df_10m['log_returns'] = np.log(df_10m['close'] / df_10m['close'].shift(1))

df_10m['volatility'] = df_10m['log_returns'].rolling(window=6).std()

df_10m.to_csv("volatility.csv", index=False)
