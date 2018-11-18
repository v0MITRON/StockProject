#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from modules import indicator
from modules import analysis


def sum_eRSI(df, analysis_df):
    
    #RSI Oversold in Uptrend
    if df['adjClose'] > df['MA200'] and df['eRSI'] <= 30:
        print('RSI oversold in uptrend')
    
    #RSI Overbought in Downtrend
    
    
    return df, analysis_df