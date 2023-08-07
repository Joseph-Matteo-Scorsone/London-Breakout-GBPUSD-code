from openbb_terminal.sdk import openbb
import pandas as pd
import matplotlib.pyplot as plt

currency_pair = openbb.forex.load(
    from_symbol='GBP',
    to_symbol='USD',
    start_date = '2023-07-31',
    end_date = '2023-08-04',
    interval = '1min')

currency_pair = currency_pair.drop(columns=['Volume'], axis=1)

#display(currency_pair.head(10))
#display(currency_pair.tail(10))

tokyoStartTime = pd.to_datetime('00:00:00').time()
tokyoEndTime = pd.to_datetime('08:00:00').time()
tokyoDF = currency_pair.between_time(tokyoStartTime, tokyoEndTime)

def calculate_tokyo_session_high_low(df):
    tokyoStartTime = pd.to_datetime('00:00:00').time()
    tokyoEndTime = pd.to_datetime('08:00:00').time()
    tokyoDF = df.between_time(tokyoStartTime, tokyoEndTime)
    
    tokyo_high = tokyoDF['Close'].max()
    tokyo_low = tokyoDF['Close'].min()
    
    return pd.Series({'Tokyo High': tokyo_high, 'Tokyo Low': tokyo_low})

# Calculate the Tokyo session high and low for each date
grouped_tokyo = currency_pair.groupby(currency_pair.index.date).apply(calculate_tokyo_session_high_low)

# Merge the calculated values back to the original dataframe
currency_pair = pd.merge(currency_pair, grouped_tokyo, left_on=currency_pair.index.date, right_index=True, how='left')

currency_pair

plt.figure(figsize=(12, 6))
plt.plot(currency_pair.index, currency_pair['Close'], label='Close', color='blue', linewidth=2)
plt.scatter(currency_pair.index, currency_pair['Tokyo High'], label='Tokyo High', color='green', marker='^', s=100)
plt.scatter(currency_pair.index, currency_pair['Tokyo Low'], label='Tokyo Low', color='red', marker='v', s=100)

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('GBP/USD Close, Tokyo High, and Tokyo Low')
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.show()

plt.savefig('NoSigsLondonBreakout.png')

plt.close()
plt.clf()

currency_pair["signal"] = 0.0

for i in range(len(currency_pair)):
    if currency_pair["Close"][i] > currency_pair["Tokyo High"][i]:
        currency_pair["signal"][i] = 1.0

    elif currency_pair["Close"][i] < currency_pair["Tokyo Low"][i]:
        currency_pair["signal"][i] = -1.0

plt.figure(figsize=(12, 6))
plt.plot(currency_pair.index, currency_pair['Close'], label='Close', color='blue', linewidth=2)
plt.scatter(currency_pair.index[currency_pair['signal'] == 1.0], currency_pair['Close'][currency_pair['signal'] == 1.0], 
            label='Buy Signal', color='white', marker='*', s=100)
plt.scatter(currency_pair.index[currency_pair['signal'] == -1.0], currency_pair['Close'][currency_pair['signal'] == -1.0], 
            label='Sell Signal', color='yellow', marker='*', s=100)
plt.scatter(currency_pair.index, currency_pair['Tokyo High'], label='Tokyo High', color='green', marker='^', s=100)
plt.scatter(currency_pair.index, currency_pair['Tokyo Low'], label='Tokyo Low', color='red', marker='v', s=100)

plt.xlabel('Date')
plt.ylabel('Price')
plt.title('GBP/USD Close, Tokyo High, Tokyo Low, and Signals')
plt.legend()
plt.grid(True)
plt.tight_layout()
#plt.show()

plt.savefig('WithSigsLondonBreakout.png')

plt.close()
plt.clf()