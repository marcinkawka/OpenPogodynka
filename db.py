import pandas as pd
import numpy as np
import sqlite3
import sys
import time
import datetime

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
			#print(sqlQuery)
			c.execute(sqlQuery)
			self.conn.commit()
			print("Sucessfully inserted "+len(gauges)+" gauges")

		except:
			#print(gauges)
			#print(type(gauges))
			print("Unexpected error:", sys.exc_info())
	
	def storeMeasurements(self,df,code):
		'''zapis df do bazy'''
		c = self.conn.cursor()
		
		try:
			df.to_sql('measurements',self.conn,if_exists='append',index_label='measurement_date')
			print("Sucessfully inserted "+df.shape[0]+" measurements")
			self.conn.commit()
		except TypeError:
			pass	
		except:
			print("Unexpected error:", sys.exc_info())

	def getMeasurementsByCode(self,df,code):
		'''extract one gauge from DataFrame and returns DataFrame indexed by time'''
		daty = df[df[0]==code].iloc[:,[3,9,5]]
		pomiary = df[df[0]==code].iloc[:,[6,7,8]]
		dd=daty[3].map(str)+" "+daty[9].map(str)+" "+daty[5].map(str)
		
		index=pd.to_datetime(dd)
		pd.DataFrame(data=pomiary)
		pomiary=pomiary.rename(columns={6:'level',7:'discharge',8:'temperature'})
		pomiary=pomiary.set_index(pd.to_datetime(dd+" 07:00"))
		pomiary=pomiary.replace('99.9','None')
		pomiary=pomiary.replace('99999.999','None')
		pomiary['gauge_code']=code
		return pomiary


	def CSVupdateHydroGauges(self):
		'''Returns list of all possible hydrological gauges, mentioned in CSV files '''
		self.gauges_DB=dict(self.getGaugesFromDB())

		for rok in range(1951,2017):
			print("Processing year "+str(rok))
			for mon in range(1,13):
				CSVfile = CSVpath+'dane_hydrologiczne/'+str(rok)+"/codz_"+str(rok)+'_'+str(mon).zfill(2)+'.csv'
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

	def CSVparseMeasurements(self):
		'''iterates through CSV files and stores data in SQLiteFile'''
		
		for rok in range(2005,2017):
			print("Processing year "+str(rok))
			for mon in range(1,13):
				CSVfile = CSVpath+'dane_hydrologiczne/'+str(rok)+"/codz_"+str(rok)+'_'+str(mon).zfill(2)+'.csv'
		
				try:
					gauges_CSV = dict(self.getGaugesFromFile(CSVfile))
					print(CSVfile)
					df = pd.read_csv(CSVfile,encoding='windows-1250',header=None)
					'''corection of year for hydrological year'''
					if mon<3:
						df[3]-=1
						
					ww=pd.DataFrame(df.loc[:,0])
					codes = ww.drop_duplicates()

					#code = 149180020
					for code in codes[0]:
						print('Processing '+str(code)+'...')
						df_measurements = self.getMeasurementsByCode(df,code)
						self.storeMeasurements(df_measurements,str(code))
					
				except OSError:
					print("Problems reading file "+CSVfile)


	def DBlistHydroGauges(self):
		''' Returns list of all hydrological gauges in 	'''
		pass