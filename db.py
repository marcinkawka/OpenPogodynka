import pandas as pd
import numpy as np
import sqlite3
import sys

from datetime import datetime
from localSettings import *


#
#  Class for feeding the sqlite database from csv files
#

class DBInterface:
	def __init__(self):
		'''Connection initialization'''
		self.conn = sqlite3.connect(SQLiteFile)

	def getGaugesFromFile(self,filename):
		'''Returns dictonary of code:gauging station name from file'''
		df = pd.read_csv(filename,encoding='windows-1250',header=None)
				#list gauges and codes
		ww=pd.DataFrame(df.loc[:,0:1])
		ww2 = ww.drop_duplicates()
		dd=dict(zip(ww2[0],ww2[1]))
		return dd	

	def getGaugesFromDB(self):
		''' returns list of tuples from DB'''
		c = self.conn.cursor()
		gauges=[]
		try:
			sqlQuery = "SELECT code,name from hydroGauges"
			for row in c.execute(sqlQuery):
				gauges.append(row)
		except:
			print("Unexpected error:", sys.exc_info())
		
		return gauges

	def storeGauges(self,gauges):
		''' Stores gauges into sqlite db'''
		c = self.conn.cursor()
		
		try:
			if len(gauges)==2:
				sqlQuery = "INSERT INTO hydroGauges VALUES {}".format(gauges)
			else:
				values = ', '.join(map(str, gauges))
				sqlQuery = "INSERT INTO hydroGauges VALUES {}".format(values)
			print(sqlQuery)
			c.execute(sqlQuery)
			self.conn.commit()
			print("Sucessfully inserted "+len(gauges)+" gauges")
		except:
			#print(gauges)
			#print(type(gauges))
			print("Unexpected error:", sys.exc_info())

	def CSVlistHydroGauges(self):
		'''Returns list of all possible hydrological gauges, mentioned in CSV files '''
		gauges_DB=dict(self.getGaugesFromDB())

		for rok in range(1951,2017):
			print("Processing year "+str(rok))
			for mon in range(1,13):
				CSVfile = CSVpath+'dane_hydrologiczne/'+str(rok)+"/codz_"+str(rok)+'_'+str(mon).zfill(2)+'.csv'
					
			#prefix=CSVpath+'dane_hydrologiczne/2014/codz_2014_05.csv'
				try:
					gauges_CSV = dict(self.getGaugesFromFile(CSVfile))

					for c in gauges_CSV.keys():
						if c in gauges_DB.keys():
							pass
							#print(str(c) +" has been found")
						else:
							newGauge = tuple((int(c),str(gauges_CSV[c])))
							print("adding "+str(newGauge[0])+" "+newGauge[1])
							self.storeGauges(newGauge)
							gauges_DB[int(newGauge[0])]=str(newGauge[1])
				except OSError:
					print("Problems reading file "+CSVfile)
		#self.storeGauges(gauges.items())
		#for k in gauges.keys():
		#	print(gauges[k])


	def DBlistHydroGauges(self):
		''' Returns list of all hydrological gauges in 	'''
		pass