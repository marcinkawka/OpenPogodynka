
import pandas as pd
import math
import numpy as np

from db import *
from localSettings import *
import datetime as dt

def convertCoordinates(lon,lat):
    x = lon * 20037508.34 / 180;
    y = math.log(math.tan((90 + lat) * math.pi / 360)) / (math.pi / 180);
    y = y * 20037508.34 / 180;
    return (x, y)





#Stary plik z IMGW ze współrzędnymi w formacie stopien,minuty,sekundy
'''
df=pd.read_excel('incoming/PSHM_30_06_2012.xls',sheetname='Hydro',skiprows=6)
lat=df['Szerokość geograficzna']+df['Unnamed: 16']/60+df['Unnamed: 17']/600
longg=df['Długość geograficzna']+df['Unnamed: 19']/60+df['Unnamed: 20']/600
'''
df=pd.read_excel('incoming/wodowskazy_BC.xls',sheetname='Arkusz1')
lat=df['lat']
longg=df['long']
code = df['KOD_SZS']

#createBokehMap(df)
d = DBInterface()
gauges = pd.DataFrame((d.getGaugesFromDB()))
gauges.columns=['code','name']
gauges.set_index('code',inplace=True)
df.set_index('KOD_SZS',inplace=True)

df2=gauges.join(df)

d.updateGaugesLocation(df2)

