from bokeh.plotting import figure, show, output_file
from bokeh.tile_providers import CARTODBPOSITRON,STAMEN_TONER
from bokeh.models import ColumnDataSource
from bokeh.models.tools import HoverTool
from bokeh.io import output_file, show
import pandas as pd
import math
import numpy as np

from db import *
from localSettings import *
import datetime as dt

def createBokehMap(df):
	'''funkcja sprawdzająca tworzy mapkę POlski z wczytanymi wodowskazami na podstawie DataFrame'''
	output_file("tile.html")


	TOOLTIPS = [
		("name","$name"),
		("river","$long"),
	]

	p = figure(x_range=(1220000, 2800000), y_range=(6100000, 7370000),
          x_axis_type="mercator", y_axis_type="mercator", tooltips=TOOLTIPS)
	p.add_tile(CARTODBPOSITRON)
	#p.add_tile(STAMEN_TONER)
	#dff=pd.DataFrame(df[['lat','long']].transpose()
	#dff=dff.rename(columns={0:'lat',1:'long',2:'x',3:'y'})
	df['x']=0.0
	df['y']=0.0
	df['x']=df['long'] * 20037508.34 / 180.0
	df['y']=np.log(np.tan((90 + df['lat']) * math.pi / 360)) / (math.pi / 180)* 20037508.34 / 180
	source=ColumnDataSource(df)
	#source = ColumnDataSource(df[['x','y','name','river']])

	p.triangle(x="x", y="y", size=4, angle=180.0,fill_color="blue", fill_alpha=0.8, source=source)
	
	#p.add_tools(HoverTool(
    #tooltips=[( 'lat','@y{custom}' )],
    #formatters=dict(y=df['y'])
	#))
	#p.add_tools(HoverTool(tooltips=["asd"]))
	show(p)

d = DBInterface()
gauges = pd.DataFrame((d.getGaugesFromDB()))
#tymczasowo poprawiam nazwy kolumn
gauges.columns=['code','name','long','lat','river']
createBokehMap(gauges)