import pandas as pd

file = "BTC-USD_2014-2023_D.csv"

# Load the historical price data into a Pandas dataframe
df = pd.read_csv(file)
prices = df['Adj Close']  # Uses close prices here

# Set the initial balance of the simulated trading account (in USD)
initial_balance_USD = 1000
initial_balance_BTC = 0
usd = initial_balance_USD
btc = initial_balance_BTC

# Set window and threshold (default 20-period and 2 STD)
window = 20
threshold = 2

# Iterate through the price data and simulate trades
for current_price in prices:
    prices_slice = prices[0:df.iloc[current_price]]
    df["MA"] = prices_slice.rolling(window=window).mean()
    z_score = (current_price - df["MA"]) / prices_slice.std()

    if z_score > threshold:
        # Make a sell order

        # Make sure there are no pending orders
        if btc > 0:
            usd += current_price * btc
            btc = 0

    elif z_score < -threshold:
        # Place a buy order for 1 Bitcoin
        if btc == 0:
            size = round(usd/current_price, -3)
            usd -= current_price*size
            btc = size

# Calculate the ROI
roi = (usd - initial_balance_USD) / initial_balance_USD
print(f"ROI: {roi:.2f}")
print(f"Final BTC balance: {btc}")
