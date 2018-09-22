import pandas as pd
import numpy as np
from modules import indicator

'''
Create analysis_df that is returned after each def and the 
big analysis comes at the end??
    if analysis_df exists:
        start making new colums
    else:
        analysis_df = pd.DataFrame({})

Create analysis matrix 1, 0, or -1 in the analysis column, 

Create def to interpret analysis matrix as sentences.
'''


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


def eval_MACD(df):
    indicator.macd(df)

    temp_df = pd.DataFrame({'fast': df['macd'],
                            'slow': df['signal'],
                            'hd': df['macd-histogram']})
    
    temp_df['abs'] = np.where(temp_df['slow'] > 0, 1, 0)
    temp_df['abs'] = np.where(temp_df['slow'] < 0, -1, temp_df['abs'])
    temp_df['macd'] = np.where(temp_df['fast'] > temp_df['slow'], 1, 0)
    temp_df['macd'] = np.where(temp_df['fast'] < temp_df['slow'], -1, temp_df['macd'])
    temp_df['diff'] = ((temp_df['fast'] - temp_df['slow']) * 100) / temp_df['slow']
    temp_df['osc'] = np.where(temp_df['hd'] > 0, 1, 0)
    temp_df['osc'] = np.where(temp_df['hd'] < 0, -1, temp_df['osc'])
   
    analysis_df = pd.DataFrame({'macd.abs': temp_df['abs'],
                                'macd.osc': temp_df['osc'],
                                'macd.sgnl': temp_df['macd'],
                                'macd.diff': temp_df['diff']})
    print(analysis_df.tail(5))
    
    print(temp_df.tail(5))

    temp_df = temp_df[-3:]
    pos = temp_df['osc'] == 1
    neg = temp_df['osc'] == -1
    bull = temp_df['macd'] == 1
    bear = temp_df['macd'] == -1
    
    if pos.any() == True:
        oscillator = "positive"
    elif neg.any() == True:
        oscillator = "negative"
    else:
        oscillator = "Neutral"
        
    if bull.any() == True:
        fast = "above"
    elif bear.any() == True:
        fast = "below"
    else:
        fast = "Neutral"
        
    mom = temp_df['diff'].iloc[2]
    
    if mom <= 5:
        momentum = "slow"
    elif mom > 5 and mom < 10:
        momentum = "average"
    elif mom >=10 and mom < 20:
        momentum = "fast"
    else:
        momentum = "extremly fast"
        
    last = temp_df['fast'].iloc[2]
    sLast = temp_df['fast'].iloc[1]
    vector = last - sLast
    if vector > 0:
        vMom = "positive"
    elif vector < 0:
        vMom = "negative"
    else:
        vMom = "undetermined"
        
    snap = temp_df['slow'].iloc[-1]
    if snap > 0:
        overall = "positive"
    elif snap < 0:
        overall = "negative"
    else:
        overall = "undetermined"

    if oscillator == "positive" and overall == "positive":
        condition = "positive"
    elif oscillator == "negative" and overall == "negative":
        condition = "negative"
    else:
        condition = "mixed"

    if condition == "mixed":
        print("MACD: Condition is currently " + condition + 
              ". The oscillator is " + oscillator + " while the MACD is "
              + overall + ". The fast EMA is trading " + fast +
              " the slow EMA with " + vMom + ", " + momentum + " momentum")

    return df, analysis_df


'''
 Evaluation w/Stochastic Oscillator
    SO:
        1 = Fast(%k) > Slow(%D)
       -1 = Fast(%k) < Slow(%D)
    SOCond (Condition):
        1 = Overbought   (x > 80)
        0 = Neutral      (80 > x < 20)
       -1 = Oversold     (x < 20)
    SOCtr:
        1 = %D above center-line (> 50)
       -1 = %D below center-line (< 50)
    SODiv:
        1 = Bullish divergence
        0 = No divergence
       -1 = Bearish divergence
    SODiff:
        Difference b/w Fast(%K) and Slow(%D).
        *Large, positive is bullish while large, negative is bearish
'''
def eval_stochastic_oscillator(df):
    indicator.stochastic_oscillator(df, 14, 3, indicator='Full')

    temp_df = pd.DataFrame({'%K': df['Slow%K_Fast%D'],
                            '%D': df['Slow%D'],
                            'close': df['adjClose']})

    temp_df['cond'] = np.where(temp_df['%D'] > 80, 1, 0)
    temp_df['cond'] = np.where(temp_df['%D'] < 20, -1, temp_df['cond'])
    temp_df['ctr'] = np.where(temp_df['%D'] > 50, 1, 0)
    temp_df['ctr'] = np.where(temp_df['%D'] < 50, -1, temp_df['ctr'])
    temp_df['sto.osc'] = np.where(temp_df['%K'] > temp_df['%D'], 1, 0)
    temp_df['sto.osc'] = np.where(temp_df['%K'] < temp_df['%D'], -1, temp_df['sto.osc'])
    temp_df['diff'] = ((temp_df['%K'] - temp_df['%D']) * 100) / temp_df['%D']
    
    #divergence
    temp_df['D1'] = np.where(temp_df['%D'].diff() > 0, 1, 0)
    temp_df['D1'] = np.where(temp_df['%D'].diff() < 0, -1, temp_df['D1'])
    temp_df['D2'] = np.where(temp_df['close'].diff() > 0, -1, 0)
    temp_df['D2'] = np.where(temp_df['close'].diff() < 0, 1, temp_df['D2'])

    temp_df['DSUM'] = temp_df['D1'] + temp_df['D2']
    #bullish divergence    
    temp_df['BLD'] = np.where(temp_df['DSUM'] == 2, 1, 0)
    #bearish divergence
    temp_df['BRD'] = np.where(temp_df['DSUM'] == -2, 1, 0)
    
    temp_df['div'] = temp_df['BLD'] + temp_df['BRD']

    analysis_df = pd.DataFrame({'SOCond': temp_df['cond'],
                                'SOCtr': temp_df['ctr'],
                                'SO': temp_df['sto.osc'],
                                'SODiff': temp_df['diff'],
                                'SODiv': temp_df['div']})
    analysis_df = analysis_df[['SO', 'SOCond', 'SOCtr', 'SODiv', 'SODiff']]

    print(analysis_df.tail(5))
    
    return df, analysis_df