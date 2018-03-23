import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

#river='Kamienna (234)'
river='Świślina (2348)'
r_short=river.split('(')[0]

df = pd.read_csv('incoming/2016/codz_2016_01.csv',encoding='windows-1250',header=None,na_values=[99999.99900000001,99.9],na_filter=True,verbose=True)

kam = df[df[2]==river]


dd=pd.to_datetime(kam[3].astype(str)+kam[9].astype(str)+kam[5].astype(str),format='%Y%m%d')

discharge_gauges = kam[1].unique()
Q_dict={}
H_dict={}
for dg in discharge_gauges:
	daty=pd.Series()
	Q=pd.Series()
	H=pd.Series()

	for rok in range(2001,2017):
		prefix = 'incoming/'+str(rok)+"/codz_"+str(rok)+'_'

		for mon in range(1,13):
			file = prefix+str(mon).zfill(2)+'.csv'
			df = pd.read_csv(file,encoding='windows-1250',header=None)
			kam = df[df[1]==dg][df[2]==river]

			if(mon<3):	#przesuniecie roku z powodu roku hydrologicznego
				shift = 1	
			else:
				shift = 0
			daty = daty.append(pd.to_datetime((kam[3]-shift).astype(str)+kam[9].astype(str)+kam[5].astype(str),format='%Y%m%d'))
			H=H.append(kam[6])
			Q=Q.append(kam[7])

		ts_Q=pd.Series(np.array(Q),index=daty)
		Q_dict[dg]=ts_Q
		ts_H=pd.Series(np.array(H),index=daty)
		H_dict[dg]=ts_H
#ts=ts.cumsum()

#	ts.plot()
#	plt.show()
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (50, 50),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'15'}
plt.rcParams.update(params)


df = pd.DataFrame(data=Q_dict)
df = df.replace({99999.99900000001:np.nan})
df.to_csv('Q_'+r_short+'.csv')

fig =df.plot()
fig.grid(True)
plt.xlabel('Calendar day', fontsize=32)
plt.ylabel('Observed discharge [m^3/s]', fontsize=32)
plt.tick_params(axis='both', which='major', labelsize=35)
plt.tick_params(axis='both', which='minor', labelsize=15)
plt.legend(loc=1, prop={'size': 36})
plt.savefig('Q_'+r_short+'.pdf',papertype='a3')

#TODO
'''
1. opisy osi
2. savowanie wyniku
3. obsługa nierównej długości ciągów
4. dynamiczny wybór posterunkow co roku
'''
#Rysowanie H chwilowo wyłączone
df = pd.DataFrame(data=H_dict)
df = df.replace({99999.99900000001:np.nan,9999:np.nan})
df.to_csv('H_'+r_short+'.csv')

fig=df.plot()
fig.grid(True)
plt.xlabel('Calendar day', fontsize=32)
plt.ylabel('Observed discharge [m^3/s]', fontsize=32)
plt.tick_params(axis='both', which='major', labelsize=35)
plt.tick_params(axis='both', which='minor', labelsize=15)
plt.legend(loc=1, prop={'size': 36})
plt.savefig('H_'+r_short+'.pdf',papertype='a3')