
from db import *
from localSettings import *

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

#print(mes)
  
#if __name__== "__main__":
#  main()
