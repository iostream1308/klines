import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df_10m = pd.read_csv('volatility_30m.csv')

df_10m['open_time'] = pd.to_datetime(df_10m['open_time'])
df_10m['close_time'] = pd.to_datetime(df_10m['close_time'])

df_10m = df_10m.dropna()

# Predicting price
df_10m['predicted_high'] = df_10m['close'] * np.exp(df_10m['volatility'])
df_10m['predicted_low'] = df_10m['close'] * np.exp(-df_10m['volatility'])

# Measuring prediction performance
df_10m['actual_next_close'] = df_10m['close'].shift(-1)
df_10m['time'] = df_10m['close_time'].shift(-1)
df_10m['pred_error_10m_high'] = np.abs(df_10m['predicted_high'] - df_10m['actual_next_close'])
df_10m['pred_error_10m_low'] = np.abs(df_10m['predicted_low'] - df_10m['actual_next_close'])

# Calculating RMSE of the predictions per hour
df_10m['rmse_increase'] = np.sqrt((df_10m['pred_error_10m_high'] ** 2).rolling(window=2).mean())
df_10m['rmse_decrease'] = np.sqrt((df_10m['pred_error_10m_low'] ** 2).rolling(window=2).mean())

print('mean of rmse_increase: ', np.mean(df_10m['rmse_increase']))
print('mean of rmse_decrease: ', np.mean(df_10m['rmse_decrease']))

df_10m = df_10m.drop(columns=['open_time', 'open', 'high', 'low', 'close', 'close_time', 'log_returns'])
df_10m = df_10m.rename(columns={'volatility': 'pre_volatility'})

df_10m.to_csv("predict_30m.csv", index=False)


# Plot the original price and the 2 predictions
plt.figure(figsize=(14, 7))
plt.plot(df_10m['time'], df_10m['actual_next_close'], label='Actual Price')
plt.plot(df_10m['time'], df_10m['predicted_high'], label='Predicted High Price', linestyle='--')
plt.plot(df_10m['time'], df_10m['predicted_low'], label='Predicted Low Price', linestyle='--')
plt.xlabel('Time')
plt.ylabel('Price')
plt.title('Actual Price vs Predicted Price')
plt.legend()
plt.show()

