import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime


#river='Kamienna (234)'
river='Świślina (2348)'
r_short=river.split('(')[0]

Q_dict={}
H_dict={}
#to trzeba przerobić, bo bez sensu pierw wybiera wodowskazy a potem iteruje po latach
for rok in range(1951,2017):
	prefix = 'incoming/'+str(rok)+"/codz_"+str(rok)+'_'

	for mon in range(1,13):
		file = prefix+str(mon).zfill(2)+'.csv'
		df = pd.read_csv(file,encoding='windows-1250',header=None)
		df_1river = df[df[2]==river]
		discharge_gauges = df_1river[1].unique()
			
		for dg in discharge_gauges:
			daty=pd.Series()
			Q=pd.Series()
			H=pd.Series()
			kam = df_1river[df_1river[1]==dg]

			if(mon<3):	#przesuniecie roku z powodu roku hydrologicznego
				shift = 1	
			else:
				shift = 0
			daty = daty.append(pd.to_datetime((kam[3]-shift).astype(str)+(kam[9].astype(int).astype(str))+(kam[5].astype(str)),format='%Y%m%d'))
				
			H=H.append(kam[6])
			Q=Q.append(kam[7])

			ts_Q=pd.Series(np.array(Q),index=daty)
			if(dg in Q_dict):
				Q_dict[dg]=Q_dict[dg].append(ts_Q)
			else:
				Q_dict[dg]=ts_Q

			ts_H=pd.Series(np.array(H),index=daty)
			if(dg in H_dict):
				H_dict[dg]=H_dict[dg].append(ts_H)
			else:
				H_dict[dg]=ts_H	
			
params = {'legend.fontsize': 'x-large',
          'figure.figsize': (50, 50),
         'axes.labelsize': 'x-large',
         'axes.titlesize':'x-large',
         'xtick.labelsize':'x-large',
         'ytick.labelsize':'15',
         'text.latex.unicode':True}
plt.rcParams.update(params)

try:
	df = pd.DataFrame(data=Q_dict)
except:
	#to jest bardzo wolne, trzeba otrajować
	df = pd.DataFrame.from_dict(Q_dict, orient='index')
	df=df.transpose()

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
1. kodowanie polskich znaków po transpozycji
'''

try:
	df = pd.DataFrame(data=H_dict)
except:
	#to jest bardzo wolne, trzeba otrajować
	df = pd.DataFrame.from_dict(H_dict, orient='index')
	df=df.transpose()

df = df.replace({99999.99900000001:np.nan,9999:np.nan})
df.to_csv('H_'+r_short+'.csv')

fig=df.plot()
fig.grid(True)
plt.xlabel('Calendar day', fontsize=32)
plt.ylabel('Observed water level [cm]', fontsize=32)
plt.tick_params(axis='both', which='major', labelsize=35)
plt.tick_params(axis='both', which='minor', labelsize=15)
plt.legend(loc=1, prop={'size': 36})
plt.savefig('H_'+r_short+'.pdf',papertype='a3')