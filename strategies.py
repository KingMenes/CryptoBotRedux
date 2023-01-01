import pandas as pd
import numpy as np


def mean_reversion(prices, window, threshold):

    # Convert the list of prices to a Pandas dataframe
    df = pd.DataFrame({"price": prices})

    # Calculate the moving average
    df["MA"] = df["price"].rolling(window=window).mean()

    # # Calculate the z-score of the prices
    z_score = (prices - df["MA"]) / df["price"].std()



    # # If the z-score is above a certain threshold, sell the asset
    # if z_score > threshold:
    #     return "SELL"
    # # If the z-score is below a certain threshold, buy the asset
    # elif z_score < -threshold:
    #     return "BUY"
    # # Otherwise, hold the asset
    # else:
    #     return "HOLD"


df = pd.read_csv("BTC-USD_2014-2023_D.csv")
mean_reversion(df['Adj Close'], 20)
