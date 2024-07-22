import pandas as pd
import requests
from datetime import datetime, timedelta

base_url = "https://api.binance.com"
endpoint = "/api/v3/klines"

def fetch_klines(symbol, interval, start_time, end_time):
    url = f"{base_url}{endpoint}"
    print(end_time)
    print(start_time)
    print("\n")
    params = {
        'symbol': symbol,
        'interval': interval,
        'startTime': start_time,
        'endTime': end_time,
        'limit' : 1000
    }
    response = requests.get(url, params=params)
    
    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return []
    
    data = response.json()
    
    return data

def fetch_all_klines(symbol, interval, start_time, end_time, delta):
    klines = []
    current_start_time = start_time
    
    while current_start_time < end_time:
        klines_batch = fetch_klines(symbol, interval, current_start_time, end_time)
        if not klines_batch:
            break
        
        klines.extend(klines_batch)
        
        current_start_time = current_start_time + delta
    
    return klines



# Define time ranges
# start time = 2024-07-21 8:00:00 GMT
start_time = 1721462400000
end_time_1hr = 1721466000000
end_time_1day = 1721548800000



# Fetch data
klines_1s = fetch_all_klines("ETHUSDT", "1s", start_time, end_time_1hr, 1000*1000)
klines_5m = fetch_all_klines("ETHUSDT", "5m", start_time, end_time_1day, 1000*300000)

# Convert to DataFrame and save to CSV
columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', 'close_time', 'quote_asset_volume', 'number_of_trades', 'taker_buy_base_asset_volume', 'taker_buy_quote_asset_volume', 'ignore']

df_1s = pd.DataFrame(klines_1s, columns=columns)
df_5s = pd.DataFrame(klines_5m, columns=columns)


df_1s.to_csv("ethusdt_1s.csv", index=False)
df_5s.to_csv("ethusdt_5m.csv", index=False)


