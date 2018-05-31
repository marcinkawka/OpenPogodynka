from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import CARTODBPOSITRON
from bokeh.models import ColumnDataSource
from bokeh.io import output_file, show
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

def createBokehMap(df):
	'''funkcja sprawdzająca tworzy mapkę POlski z wczytanymi wodowskazami na podstawie DataFrame'''
	output_file("tile.html")
	p = figure(x_range=(1220000, 2800000), y_range=(6100000, 7370000),
          x_axis_type="mercator", y_axis_type="mercator")
	p.add_tile(CARTODBPOSITRON)
	
	dff=pd.DataFrame([lat,longg]).transpose()
	dff=dff.rename(columns={0:'lat',1:'long',2:'x',3:'y'})
	dff['x']=0
	dff['y']=0
	dff['x']=dff['long'] * 20037508.34 / 180
	dff['y']=np.log(np.tan((90 + dff['lat']) * math.pi / 360)) / (math.pi / 180)* 20037508.34 / 180
	source = ColumnDataSource(dff[['x','y']])

	p.circle(x="x", y="y", size=4, fill_color="blue", fill_alpha=0.8, source=source)
	show(p)




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

