import pandas as pd
import numpy as np
import datetime


def sma(df, period):
    label = 'MA' + str(period)
    
    df[label] = np.round(df['adjClose'].rolling(window = period, center=False).mean(), 2)

    return df


def ema(df, period):
    label = 'EMA' + str(period)

    df[label] = df['adjClose'].ewm(span=20, min_periods=period).mean()

    return df


def rsi(df, period):
    close = df['adjClose']
    # Get the diff in price from previous step
    delta = close.diff()
    # Get rid of the first row, which is NaN
    delta = delta[1:]
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    # Calculate the SMA
    roll_up = up.rolling(period).mean()
    roll_down = down.abs().rolling(period).mean()
    # Calculate the RSI based on SMA
    RS = roll_up / roll_down
    RSI = 100.0 - (100.0 / (1.0 + RS))
    
    df['RSI'] = RSI
    
    return df


if __name__ == "__main__":
    print("Hello World")
#