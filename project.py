import pandas as pd 
import numpy as np 
#data = pd.read_csv('mine.txt', delimiter=" ", header=None)
df1 = pd.read_table('mine.txt', delim_whitespace=True , header=None , names=('Flowrate', 'PressureDrop', 'EntryTemp' , 'ExitTemp', 'OppositeEntryTemp'))

df2 = pd.read_table('mine2.txt', delim_whitespace=True , header=None , names=('Flowrate', 'PressureDrop', 'EntryTemp' , 'ExitTemp', 'OppositeEntryTemp'))


df_all = pd.concat([df1.set_index('Flowrate'), df2.set_index('Flowrate')],axis='columns', keys=['First', 'Second'])
df_final = df_all.swaplevel(axis='columns')[df1.columns[1:]]

def highlight_diff(data, color='yellow'):
    attr = 'background-color: {}'.format(color)
    other = data.xs('First', axis='columns', level=-1)
    return pd.DataFrame(np.where(data.ne(other, level=0), attr, ''),
                        index=data.index, columns=data.columns)
df_final.style.apply(highlight_diff, axis=None)
df3 = df1.merge(df2, how='outer', on='Flowrate', suffixes=['_1', '_2'])
df3['check'] = df3.PressureDrop_1 == df3.PressureDrop_2
from pandas import ExcelWriter

writer = ExcelWriter('PythonExport1.xlsx')
df3.to_excel(writer,'Sheet5')
writer.save()