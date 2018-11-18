import pandas as pd
import numpy as np


def sma(df, period):
    label = 'MA' + str(period)

    df[label] = np.round(df['adjClose'].rolling(window=period).mean(), 2)

    return df


def ema(df, period):
    label = 'EMA' + str(period)

    weight = (2 / (period + 1))

    df[label] = df['adjClose'].ewm(alpha=weight, min_periods=period).mean()

    return df


def sma_vol(df, period):
    label = 'volMA' + str(period)

    df[label] = np.round(df['adjVolume'].rolling(window=period).mean(), 2)

    return df


def ema_vol(df, period):
    label = 'volEMA' + str(period)

    weight = (2 / (period + 1))

    df[label] = df['adjVolume'].ewm(alpha=weight, min_periods=period).mean()

    return df


def RSI(df, period):
    temp_df = pd.DataFrame({'close': df['adjClose']})

    weight = (2 / (period + 1))

    temp_df['delta'] = temp_df['close'].diff()
    temp_df['up/down'] = np.where(temp_df['delta'] > 0, 1, -1)
    temp_df['gain'] = np.where(temp_df['up/down'] > 0,
                               temp_df['delta'], 0)
    temp_df['loss'] = np.where(temp_df['up/down'] < 0,
                               temp_df['delta'].abs(), 0)
    temp_df['periodGain'] = temp_df['gain'].ewm(alpha=weight,
                                                min_periods=period).mean()
    temp_df['periodLoss'] = temp_df['loss'].ewm(alpha=weight,
                                                min_periods=period).mean()

    temp_df['RS'] = temp_df['periodGain'] / temp_df['periodLoss']
    df['RSI'] = np.round((100 - 100/(1 + temp_df['RS'])), 4)

    graph_df = pd.DataFrame({'RSI': df['RSI']})

    graph_df.tail(120).plot(grid=True)

    return df


def eRSI(df, period):
    temp_df = pd.DataFrame({'close': df['adjClose']})

    temp_df['delta'] = temp_df['close'].diff()
    temp_df['up/down'] = np.where(temp_df['delta'] > 0, 1, -1)
    temp_df['gain'] = np.where(temp_df['up/down'] > 0,
                               temp_df['delta'], 0)
    temp_df['loss'] = np.where(temp_df['up/down'] < 0,
                               temp_df['delta'].abs(), 0)
    temp_df['periodGain'] = temp_df['gain'].rolling(period).mean()
    temp_df['periodLoss'] = temp_df['loss'].rolling(period).mean()

    temp_df['RS'] = temp_df['periodGain'] / temp_df['periodLoss']
    df['eRSI'] = np.round((100 - 100/(1 + temp_df['RS'])), 4)

    graph_df = pd.DataFrame({'eRSI': df['eRSI']})

    graph_df.tail(120).plot(grid=True)

    return df


def macd(df):
    ema(df, 12)
    ema(df, 26)

    temp_df = pd.DataFrame({'EMA12': df['EMA12'],
                            'EMA26': df['EMA26']})

    temp_df['macd'] = temp_df['EMA12'] - temp_df['EMA26']

    weight = (2 / (9 + 1))
    temp_df['signal'] = temp_df['macd'].ewm(alpha=weight, min_periods=9).mean()
    temp_df['macd-histogram'] = temp_df['macd'] - temp_df['signal']

    macd_df = pd.DataFrame({'macd': temp_df['macd'],
                            'signal': temp_df['signal'],
                            'macd-histogram': temp_df['macd-histogram']})

    macd_df.tail(120).plot(grid=True)

    df['macd'] = temp_df['macd']
    df['signal'] = temp_df['signal']
    df['macd-histogram'] = temp_df['macd-histogram']

    return df


def bollinger_bands(df, period):
    sma(df, period)
    std_dev = np.round(df['adjClose'].rolling(window=period).std(), 2)
    label = 'MA' + str(period)

    df['mid_band'] = df[label]
    df['upp_band'] = df[label] + (std_dev * 2)
    df['low_band'] = df[label] - (std_dev * 2)

    bd_df = pd.DataFrame({'mid': df['mid_band'],
                                 'upp': df['upp_band'],
                                 'low': df['low_band'],
                                 'close': df['adjClose']})

    bd_df.tail(120).plot(grid=True)

    return df, bd_df


def stochastic_oscillator(df, period, smooth, indicator):
    temp_df = df

    temp_df['maxhigh'] = df['adjClose'].rolling(window=period).max()
    temp_df['minlow'] = df['adjClose'].rolling(window=period).min()
    df['%K'] = (df['adjClose'] - temp_df['minlow']) / (temp_df['maxhigh'] - temp_df['minlow']) * 100
    df['Slow%K_Fast%D'] = df['%K'].rolling(window=smooth).mean()
    df['Slow%D'] = df['Slow%K_Fast%D'].rolling(window=smooth).mean()

    if indicator == 'Fast':
        graph_df = pd.DataFrame({'%K': df['%K'],
                                 '%D': df['Slow%K_Fast%D']})
    elif indicator == 'Slow':
        graph_df = pd.DataFrame({'%K': df['Slow%K_Fast%D'],
                                 '%D': df['Slow%D']})
    elif indicator == 'Full':
        graph_df = pd.DataFrame({'%K': df['Slow%K_Fast%D'],
                                 '%D': df['Slow%D']})
    else:
        raise ValueError('indicator values can only {"Fast", "Slow", "Full"}')

    graph_df.tail(120).plot(grid=True)

    return df


def mfi(df, period):
    temp_df = pd.DataFrame({'high': df['adjHigh'],
                            'low': df['adjLow'],
                            'close': df['adjClose'],
                            'volume': df['adjVolume']})

    temp_df['typicalPrice'] = (temp_df['high'] + temp_df['low'] + temp_df['close']) / 3
    temp_df['raw$flow'] = temp_df['typicalPrice'] * temp_df['volume']

    temp_df['delta'] = temp_df['typicalPrice'].diff()
    temp_df['up/down'] = np.where(temp_df['delta'] > 0, 1, -1)
    temp_df['+$Flow'] = np.where(temp_df['up/down'] > 0,
                                 temp_df['raw$flow'], 0)
    temp_df['-$Flow'] = np.where(temp_df['up/down'] < 0,
                                 temp_df['raw$flow'], 0)
    temp_df['period+$flow'] = temp_df['+$Flow'].rolling(period).sum()
    temp_df['period-$flow'] = temp_df['-$Flow'].rolling(period).sum()

    temp_df['moneyFlowRatio'] = temp_df['period+$flow'] / temp_df['period-$flow']
    df['moneyFlowIndex'] = np.round((100 - 100/(1 + temp_df['moneyFlowRatio'])), 4)

    graph_df = pd.DataFrame({'MFI': df['moneyFlowIndex']})

    graph_df.tail(120).plot(grid=True)

    return df


def chaikin_oscillator(df, f, s):

    temp_df = pd.DataFrame({'high': df['adjHigh'],
                            'low': df['adjLow'],
                            'close': df['adjClose'],
                            'volume': df['adjVolume']})

    temp_df['$flowX'] = ((temp_df['close'] - temp_df['low']) - (temp_df['high'] - temp_df['close'])) /(temp_df['high'] - temp_df['low'])
    temp_df['$flowVol'] = temp_df['$flowX'] * temp_df['volume']

    temp_df['ADL'] = 0
    temp_df['ADL'] = temp_df['ADL'].shift(periods=-1, axis=0) + temp_df['$flowVol']

    fweight = 2 / (f + 1)
    sweight = 2 / (s + 1)

    fast = temp_df['ADL'].ewm(alpha=fweight, min_periods=f).mean()
    slow = temp_df['ADL'].ewm(alpha=sweight, min_periods=s).mean()

    df['ChaikinOsc'] = fast - slow

    graph_df = pd.DataFrame({'Chaikin Oscillator': df['ChaikinOsc']})

    graph_df.tail(60).plot(grid=True)

    return df


if __name__ == "__main__":
    print("Hello World")
#
