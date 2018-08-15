import pandas as pd
import numpy as np
from modules import indicator


def ema_group(df):
    indicator.ema(df, 10)
    indicator.ema(df, 50)
    indicator.ema(df, 90)
    indicator.ema(df, 200)

    return df


def eval_group(df, group):
    if group == 'week':
        ptime = 'W'
        peval = 'weekly_df'
    elif group == 'month':
        ptime = 'M'
        peval = 'monthly_df'
    elif group == 'quarter':
        ptime = 'Q'
        peval = 'quarterly_df'
    elif group == 'year':
        ptime = 'A'
        peval = 'yearly_df'
    else:
        raise ValueError('group values can only be {"week", "month", "quarter", "year"}')

    temp_df = pd.DataFrame({'open': df['adjOpen'],
                            'low': df['adjLow'],
                            'high': df['adjHigh'],
                            'close': df['adjClose'],
                            'volume': df['adjVolume']})

    p_open = temp_df['open'].resample(ptime, closed='left').agg(lambda x: x[0])
    p_max = temp_df.groupby(pd.Grouper(freq=ptime)).high.max()
    p_min = temp_df.groupby(pd.Grouper(freq=ptime)).low.min()
    p_close = temp_df['close'].resample(ptime).agg(lambda x: x[-1])
    p_volume = temp_df.groupby(pd.Grouper(freq=ptime)).volume.sum()
    p_diff = p_close.diff()
    p_pct = p_close.pct_change().mul(100)

    p_end = pd.DataFrame({'High': p_max,
                          'Low': p_min,
                          'Close': p_close,
                          'Volume': p_volume,
                          'Delta': p_diff,
                          'Pct Change': p_pct
                         })

    p_end = p_end[['High', 'Low', 'Close', 'Volume', 'Delta', 'Pct Change']]
    p_start = pd.DataFrame({'Open': p_open, })

    p_periodStart = p_start.to_period(freq=ptime)
    p_periodEnd = p_end.to_period(freq=ptime)

    peval = pd.merge(p_periodStart, p_periodEnd,
                     left_index=True, right_index=True)

    return peval

'''
 General case to be used for either RSI or eRSI.
 ***Needs further testing to verify accurate condition results***
'''
def RSI_condition(df):
#    temp_df = pd.DataFrame({'RSI': df['RSI']})
#    temp_df = temp_df[-3:]
    temp_df = df[-3:]
    temp_df['condition'] = np.where(temp_df[0:3] > 70, 1, 0)
    temp_df['condition'] = np.where(temp_df[0:3] < 30, -1, temp_df['condition'])

    ob = temp_df['condition'] == 1
    os = temp_df['condition'] == -1
    
    if ob.any() == True:
        condition = "Overbought"
    elif os.any() == True:
        condition = "Oversold"
    else:
        condition = "Neutral"
    
    return condition


def eval_RSI(df, period):
    indicator.RSI(df, period) 
    condition = RSI_condition(df['RSI'])
    print("RSI: Condition is currently " + condition)
    
    return df


def eval_eRSI(df, period):
    indicator.eRSI(df, period)
    condition = RSI_condition(df['eRSI'])
    print("eRSI: Condition is currently " + condition)
    
    return df
