import time
from coinbase.wallet.client import Client

# Replace these with your own Coinbase Pro API keys
API_KEY = "your-api-key"
API_SECRET = "your-api-secret"

# Connect to Coinbase Pro
client = Client(API_KEY, API_SECRET)

# Set the Coinbase Pro product ID for Bitcoin
product_id = "BTC-USD"

# Set the mean reversion parameters (mean and standard deviation)
mean = 0
std_dev = 0

while True:
  # Fetch the current Bitcoin price
  current_price = client.get_product_ticker(product_id=product_id)["price"]

  # Calculate the upper and lower bounds
  upper_bound = mean + 2 * std_dev
  lower_bound = mean - 2 * std_dev

  # Check if the current price is outside the bounds
  if current_price > upper_bound:
    # Place a sell order
    client.sell(price=current_price, size=1, product_id=product_id)

    # Update the mean and standard deviation
    mean, std_dev = update_mean_std_dev(mean, std_dev, current_price)

  elif current_price < lower_bound:
    # Place a buy order
    client.buy(price=current_price, size=1, product_id=product_id)

    # Update the mean and standard deviation
    mean, std_dev = update_mean_std_dev(mean, std_dev, current_price)

  # Sleep for an hour before checking the price again
  time.sleep(3600)



