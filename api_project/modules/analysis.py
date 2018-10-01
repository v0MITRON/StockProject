import pandas as pd
import numpy as np
from modules import indicator

'''
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
                          'Pct Change': p_pct})

    p_end = p_end[['High', 'Low', 'Close', 'Volume', 'Delta', 'Pct Change']]
    p_start = pd.DataFrame({'Open': p_open, })

    p_periodStart = p_start.to_period(freq=ptime)
    p_periodEnd = p_end.to_period(freq=ptime)

    peval = pd.merge(p_periodStart, p_periodEnd,
                     left_index=True, right_index=True)

    return peval

'''
 Common analysis:
     temp_df['dir'] - direction up/down
     temp_df['cond'] - condition (overbought/oversold; )
     temp_df['Xcond'] - extreme condition
     temp_df['abs'] - absolute, above/below zero line
     temp_df['div'] - bull/bear divergences
'''

temp_df = pd.DataFrame({})

def pnc(temp_df, g=0, l=0, diff=False, tc='x', Nc='y'):
    if diff == True:
        temp_df[Nc] = np.where(temp_df[tc].diff() > g, 1, 0)
        temp_df[Nc] = np.where(temp_df[tc].diff() < l, -1, temp_df[Nc])
    else:
        temp_df[Nc] = np.where(temp_df[tc] > g, 1, 0)
        temp_df[Nc] = np.where(temp_df[tc] < l, -1, temp_df[Nc])
    
    return temp_df[Nc]

def direction(temp_df, c='x'):
#    temp_df['dir'] = np.where(temp_df[c].diff() > 0, 1, 0)
#    temp_df['dir'] = np.where(temp_df[c].diff() < 0, -1, temp_df['dir'])
    temp_df['dir'] = pnc(temp_df, g=0, l=0, diff=True, tc=c, Nc='dir')

    return temp_df['dir']


def condition(temp_df, ob, os, c='x'):
#    temp_df['cond'] = np.where(temp_df[c] > ob, 1, 0)
#    temp_df['cond'] = np.where(temp_df[c] < os, -1, temp_df['cond'])
    temp_df['cond'] = pnc(temp_df, g=ob, l=os, diff=False, tc=c, Nc='cond')

    return temp_df['cond']


def divergence(temp_df, c='x'):
    #divergence
    temp_df['D1'] = np.where(temp_df[c].diff() > 0, 1, 0)
    temp_df['D1'] = np.where(temp_df[c].diff() < 0, -1, temp_df['D1'])
    temp_df['D2'] = np.where(temp_df['close'].diff() > 0, -1, 0)
    temp_df['D2'] = np.where(temp_df['close'].diff() < 0, 1, temp_df['D2'])

    temp_df['DSUM'] = temp_df['D1'] + temp_df['D2']
    #bullish divergence    
    temp_df['BLD'] = np.where(temp_df['DSUM'] == 2, 1, 0)
    #bearish divergence
    temp_df['BRD'] = np.where(temp_df['DSUM'] == -2, 1, 0)
    
    temp_df['div'] = temp_df['BLD'] + temp_df['BRD']
    
    return temp_df['div']

'''
 General case to be used for eithe RSI or eRSI.
 ***Needs further testing to verrify accurate condition results***
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
        cond = "Overbought"
    elif os.any() == True:
        cond = "Oversold"
    else:
        cond = "Neutral"
    
    return cond


def eval_RSI(df, period, analysis_df):
    indicator.RSI(df, period) 
#    cond = RSI_condition(df['RSI'])
#    print("RSI: Condition is currently " + cond)

    temp_df = pd.DataFrame({'RSI': df['RSI']})
    temp_df['cond'] = condition(temp_df, ob=70, os=30, c='RSI')
    
    analysis_df['RSIcond'] = temp_df['cond']
    
    return df, analysis_df


def eval_eRSI(df, period, analysis_df):
    indicator.eRSI(df, period)
#    cond = RSI_condition(df['eRSI'])
#    print("eRSI: Condition is currently " + cond)

    temp_df = pd.DataFrame({'RSI': df['eRSI']})
    temp_df['cond'] = condition(temp_df, ob=70, os=30, c='RSI')
    
    analysis_df['eRSIcond'] = temp_df['cond']
    
    return df, analysis_df


def eval_MACD(df, analysis_df):
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
   
    analysis_df['MACDabs'] = temp_df['abs']
    analysis_df['MACDosc'] = temp_df['osc']
    analysis_df['MACDsgnl'] = temp_df['macd']
    analysis_df['MACDdiff'] = temp_df['diff']

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
        print("MACD: Condition is currently " + condition + 
              " with the oscillator & MACD " + oscillator + 
              ". The fast EMA is trading " + fast +
              " the slow EMA with " + vMom + ", " + momentum + " momentum")
    elif oscillator == "negative" and overall == "negative":
        condition = "negative"
        print("MACD: Condition is currently " + condition + 
              " with the oscillator & MACD " + oscillator + 
              ". The fast EMA is trading " + fast +
              " the slow EMA with " + vMom + ", " + momentum + " momentum")
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
def eval_stochastic_oscillator(df, analysis_df):
    indicator.stochastic_oscillator(df, 14, 3, indicator='Full')

    temp_df = pd.DataFrame({'%K': df['Slow%K_Fast%D'],
                            '%D': df['Slow%D'],
                            'close': df['adjClose']})

    temp_df['cond'] = condition(temp_df, ob=80, os=20, c='%D')
    temp_df['ctr'] = np.where(temp_df['%D'] > 50, 1, 0)
    temp_df['ctr'] = np.where(temp_df['%D'] < 50, -1, temp_df['ctr'])
    temp_df['sto.osc'] = np.where(temp_df['%K'] > temp_df['%D'], 1, 0)
    temp_df['sto.osc'] = np.where(temp_df['%K'] < temp_df['%D'], -1, temp_df['sto.osc'])
    temp_df['diff'] = ((temp_df['%K'] - temp_df['%D']) * 100) / temp_df['%D']
    
    temp_df['div'] = divergence(temp_df, c='%D')
  
    analysis_df['SOCond'] = temp_df['cond']
    analysis_df['SOCtr'] = temp_df['ctr']
    analysis_df['SO'] = temp_df['sto.osc']
    analysis_df['SODiff'] = temp_df['diff']
    analysis_df['SODiv'] = temp_df['div']
    
    return df, analysis_df


def eval_bollinger_bands(df, analysis_df):
    indicator.bollinger_bands(df, 20)
    
    bd_df = pd.DataFrame({'mid': df['mid_band'],
                          'upp': df['upp_band'],
                          'low': df['low_band'],
                          'close': df['adjClose']})
    
    bd_df['ctr'] = np.where(bd_df['close'] > bd_df['mid'], 1, 0)
    bd_df['ctr'] = np.where(bd_df['close'] < bd_df['mid'], -1, bd_df['ctr'])
    bd_df['uR'] = (bd_df['upp'] - (bd_df['upp'] * .02))
    bd_df['lR'] = (bd_df['low'] + (bd_df['low'] * .02))
    bd_df['cond'] = np.where(bd_df['close'] > bd_df['uR'], 1, 0) 
    bd_df['cond'] = np.where(bd_df['close'] < bd_df['lR'], -1, bd_df['cond'])
    bd_df['Xcond'] = np.where(bd_df['close'] > bd_df['upp'], 1, 0) 
    bd_df['Xcond'] = np.where(bd_df['close'] < bd_df['low'], -1, bd_df['Xcond'])
    
    analysis_df['BBCtr'] = bd_df['ctr']
    analysis_df['BBCond'] = bd_df['cond']
    analysis_df['BBXcond'] = bd_df['Xcond']
    
    return df, analysis_df


def eval_mfi(df, analysis_df):
    indicator.mfi(df, 14)
    
    temp_df = pd.DataFrame({'close': df['adjClose'],
                            'mfi': df['moneyFlowIndex']})
    
    temp_df['Ncond'] = condition(temp_df, ob=80, os=20, c='mfi')
    temp_df['Xcond'] = condition(temp_df, ob=89, os=11, c='mfi')
    temp_df['div'] = divergence(temp_df, c='mfi')
    
    analysis_df['MFIcond'] = temp_df['Ncond']
    analysis_df['MFIXcond'] = temp_df['Xcond']
    analysis_df['MFIdiv'] = temp_df['div']
    
    return df, analysis_df


def eval_chaikin_oscillator(df, analysis_df):
    indicator.chaikin_oscillator(df, 6, 20)
    
    temp_df = pd.DataFrame({'close': df['adjClose'],
                            'cho': df['ChaikinOsc']})

    temp_df['osc'] = np.where(temp_df['cho'] > 0, 1, 0)
    temp_df['osc'] = np.where(temp_df['cho'] < 0, -1, temp_df['osc'])
    
    temp_df['dir'] = direction(temp_df, c='cho')
    temp_df['div'] = divergence(temp_df, c='cho')
    
    analysis_df['CO'] = temp_df['osc']
    analysis_df['COdir'] = temp_df['dir']
    analysis_df['COdiv'] = temp_df['div']

    return df, analysis_df


def eval_matrix(analysis_df):
#run all evals    
    return analysis_df

def eval_analysis(analysis_df):
#interpret the matrix!    
    return analysis_df