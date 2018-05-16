#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 15 21:37:59 2018

@author: matt
"""

from urllib.request import urlopen, Request
import pandas as pd
from pandas_datareader import data as web
import datetime
import h5py
import numpy as np

file = '/home/matt/AnacondaProjects/h5pyTests/DDD.h5'

table = pd.read_hdf(file, 'table')

print(table.tail(10))