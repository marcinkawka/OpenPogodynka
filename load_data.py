import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime



df = pd.read_csv('incoming/codz_2016_01.csv',encoding='windows-1250',header=None,na_values=[99999.99900000001,99.9],na_filter=True,verbose=True)

kam = df[df[2]=='Kamienna (234)']

dd=pd.to_datetime(kam[3].astype(str)+kam[9].astype(str)+kam[5].astype(str),format='%Y%m%d')

discharge_gauges = kam[1].unique()

prefix = 'incoming/codz_2016_'
dd={}
for dg in discharge_gauges:

	daty=pd.Series()
	Q=pd.Series()
	H=pd.Series()

	for mon in range(1,13):
		file = prefix+str(mon).zfill(2)+'.csv'
		df = pd.read_csv(file,encoding='windows-1250',header=None)
		kam = df[df[1]==dg][df[2]=='Kamienna (234)']

		if(mon<3):	#przesuniecie roku z powodu roku hydrologicznego
			shift = 1	
		else:
			shift = 0
		daty = daty.append(pd.to_datetime((kam[3]-shift).astype(str)+kam[9].astype(str)+kam[5].astype(str),format='%Y%m%d'))
		H=H.append(kam[6])
		Q=Q.append(kam[7])

	ts=pd.Series(np.array(Q),index=daty)
	dd[dg]=ts
#ts=ts.cumsum()

#	ts.plot()
#	plt.show()

df = pd.DataFrame(data=dd)
df=df.replace({99999.99900000001:np.nan})

df.plot()
plt.savefig('asdf.pdf',papertype='a3')
