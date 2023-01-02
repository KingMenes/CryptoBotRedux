import pandas as pd
import numpy as np
from helperFunctions import moving_average

file = "BTC-USD_2014-2023_D.csv"

# Load the historical price data into a Pandas dataframe
df = pd.read_csv(file)
prices = df['Adj Close'].to_numpy()  # Uses close prices here

# Set the initial balance of the simulated trading account (in USD)
initial_balance_USD = 1000
initial_balance_BTC = 0
usd = initial_balance_USD
btc = initial_balance_BTC
buy_trades = 0
sell_trades = 0
account_value = 0

# Set window and threshold (default 20-period and 2 STD)
window = 20
threshold = 1

# Iterate through the price data and simulate trades
for current_price in prices:
    # Check if current_price is in the prices array
    index = np.where(prices == current_price)
    if len(index[0]) == 0:
        # current_price is not in the prices array
        continue
    else:
        # current_price is in the prices array
        index = index[0][0]

    # Slice the prices array up to the index of current_price
    prices_slice = prices[:index]

    # Calculate moving average based on a window
    ma = moving_average(prices_slice, window)
    if len(ma) > 0:
        z_score = (current_price - ma[-1]) / np.std(prices_slice)
        # print(f"Z-score: {z_score:.2f} MA: {ma} ")

        if z_score > threshold:
            # Make a sell order

            # Make sure there are no pending orders
            if btc > 0:
                size = btc
                usd += current_price * size
                sell_trades += 1
                print(
                    f"Sold {size} BTC at {current_price} for a total of {size * current_price} | Current account: {btc - size}"
                    f" BTC {usd} USD")
                btc = 0


        elif z_score < -threshold:
            # Place a buy order
            if btc == 0:
                size = float(format(usd / current_price, '.3f')) - 0.001
                usd -= current_price * size
                btc += size
                buy_trades += 1
                print(
                    f"Bought {size} BTC at {current_price} for a total of {size * current_price} | Current account: {btc} BTC {usd} USD")
                account_value = btc * current_price

# Calculate the ROI
if (btc > 0):
    roi = (account_value - initial_balance_USD) / initial_balance_USD * 100
else:
    roi = (usd - initial_balance_USD) / initial_balance_USD * 100

# Print Results
print(f"\nFinal BTC balance: {btc}")
print(f"Account Value: ${account_value}")
print(f"ROI: {roi:.2f}%")
print(f"Total Trades: {buy_trades + sell_trades} | Buys: {buy_trades} | Sells:{sell_trades}")
