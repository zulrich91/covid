import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy.integrate import odeint


BASE = './data/27-08_2020/'
AGGREG=BASE+'/aggreg/'
INPUT = AGGREG+'agg_data_per_days.csv'
OUTPUT = AGGREG+'sir_per_day.csv'


df = pd.read_csv(INPUT)
df['I'] = df['incid_hosp'] + df['incid_rea']
df['R'] = df['incid_rad'] + df['incid_dc']

df_sir = df[['jour', 'I','R']]
df_sir['S'] = 66000000

for index in df_sir.index:
    if index == df_sir.index.min():
        df_sir.loc[index, 'S'] = 66000000 - (df_sir.loc[index, 'I'] + df_sir.loc[index, 'R'])
    elif(index < df_sir.index.max()):
        df_sir.loc[index, 'S'] = df_sir.loc[index-1, 'S'] - (df_sir.loc[index, 'I'] + df_sir.loc[index, 'R'])
df_sir.sort_values('jour', inplace=True)
df_sir.to_csv(OUTPUT,index=False)

