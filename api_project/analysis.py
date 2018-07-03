import pandas as pd
import numpy as np
import datetime


def sma(df, period):
    label = 'MA' + str(period)
    
    df[label] = np.round(df['adjClose'].rolling(window = period, center=False).mean(), 2)

    return df


def ema(df, period):
    label = 'EMA' + str(period)
    
    weight = (2 / (period + 1))

    df[label] = df['adjClose'].ewm(alpha=weight, min_periods=period).mean()

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


def macd(df):
    ema(df, 12)
    ema(df, 26)
    
    temp_df = pd.DataFrame({'EMA12': df['EMA12'],
                            'EMA26': df['EMA26']})
    
    temp_df['macd'] = temp_df['EMA12'] - temp_df['EMA26']
    
    weight = (2 / (9 + 1))
    temp_df['signal'] = temp_df['macd'].ewm(alpha=weight, min_periods=9).mean()
    
    macd_df = pd.DataFrame({'macd': temp_df['macd'],
                            'signal': temp_df['signal']})
    
    macd_df.tail(120).plot(grid=True)


if __name__ == "__main__":
    print("Hello World")
#
