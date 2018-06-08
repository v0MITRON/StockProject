import pandas as pd
import numpy as np
import datetime


def sma(df, period):
    label = 'MA' + str(period)
    
    df[label] = df['adjClose'].rolling(period).mean()

    return df


def ema(df, period):
    label = 'EMA' + str(period)

    df[label] = pd.ewma(df['adjClose'], span=20, min_periods=period)

    return df


if __name__ == "__main__":
    print("Hello World")
