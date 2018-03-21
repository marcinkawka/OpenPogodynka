import pandas as pd
import numpy as np
from datetime import datetime

df = pd.read_csv('codz_2016_01.csv')

df = pd.read_csv('incoming/codz_2016_01.csv',encoding='windows-1250',header=None)

kam = df[df[2]=='Kamienna (234)']

kam_dat = pd.Timestamp(datetime(kam[3],kam[9],kam[5]))