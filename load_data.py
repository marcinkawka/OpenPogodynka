import pandas as pd
import numpy as np
from datetime import datetime




df = pd.read_csv('incoming/codz_2016_01.csv',encoding='windows-1250',header=None)

kam = df[df[2]=='Kamienna (234)']

kam_dat = pd.Timestamp(datetime(kam[3],kam[9],kam[5]))
pd.to_datetime(kam[3],format='%Y')+pd.to_datetime(kam[9],format='%m')

pd.to_datetime([kam[3],kam[9]],format='%Y%m')
pd.to_datetime(df.year*10000 + df.month*100 + df.day, format='%Y%m%d')
pd.to_datetime(kam[0:4][[3,9,5]],format='%Y%m')