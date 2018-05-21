
from db import *
from localSettings import *
import datetime as dt

'''skrypt do obliczeń na bazie danyc'''

#def main():
d = DBInterface()
print("Hello World!")
gauges = dict(d.getGaugesFromDB())
'''
TODO:
1. iteracja po codach
'''
codes = [152210010,152210040,152200110]
def calculateMonthly():
	for code in codes:
		mQ=[]
		mes=d.getMeasurementsFromDB(code)
		mes['temperature'].replace('None', np.nan, inplace=True)
		mes['level'].replace('None', np.nan, inplace=True)
		mes['discharge'].replace('None', np.nan, inplace=True)

		mes=mes.convert_objects(convert_numeric=True)

		df_mean=mes.groupby(pd.Grouper(freq='M')).mean()
		df_mean=df_mean.dropna(how='all')

		df_min=mes.groupby(pd.Grouper(freq='M')).min()
		df_min=df_min.dropna(how='all')

		df_max=mes.groupby(pd.Grouper(freq='M')).max()
		df_max=df_max.dropna(how='all')

		df_median=mes.groupby(pd.Grouper(freq='M')).median()
		df_median=df_median.dropna(how='all')

		df_max.columns=['WQ','WT','WW']
		df_min.columns=['NQ','NT','NW']
		df_median.columns=['ZQ','ZT','ZW']
		df_mean.columns=['SQ','ST','SW']

		df=pd.concat([df_max,df_min,df_median,df_mean],axis=1)

		mT = df[['NT','ST','ZT','WT']].copy()
		mQ = df[['NQ','SQ','ZQ','WQ']].copy()
		mW = df[['NW','SW','ZW','WW']].copy()

		mQ['gauge_code']=code
		mW['gauge_code']=code
		mT['gauge_code']=code
		mW=mW.dropna(axis=0, how='any')
		mT=mT.dropna(axis=0, how='any')
		mQ=mQ.dropna(axis=0, how='any')

		d.storeDischargeAgregates(mQ)

roki = [1951,1952,1953]
codes= [152210010]
#def calculateYearly():
for code in codes:	
	mQ=[]
	mes=d.getMonthlyStatsFromDB(code)
	#mes['temperature'].replace('None', np.nan, inplace=True)
	mes=mes.convert_objects(convert_numeric=True)
	mes["measurement_date"]=pd.to_datetime(mes["measurement_date"])

	rok=1953
	przeplywy = pd.DataFrame(columns=('WWQ','SWQ','SSQ','SNQ','NNQ'))
	
	for rok in range(1952,2016):
		maska_roku_hydro =  ((dt.datetime(rok-1,11,1)<mes["measurement_date"]) & ( mes["measurement_date"]<dt.datetime(rok,11,1)))
		roczny_mes= mes[maska_roku_hydro]
		WWQ=roczny_mes["WQ"].max()
		SWQ=roczny_mes["WQ"].mean()
		SSQ=roczny_mes["SQ"].mean()
		SNQ=roczny_mes["NQ"].mean()
		NNQ=roczny_mes["NQ"].min()
		przeplywy.loc[rok]=[WWQ,SWQ,SSQ,SNQ,NNQ]
		'''
		TODO: 1.Zapis do SQLa
			2. Agregaty półroczne	
		'''
		
	przeplywy.dropna(inplace=True)		

#print(mes)
#def main():
#	calculateYearly()
  
#if __name__== "__main__":
#  main()
