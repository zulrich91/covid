import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy.integrate import odeint


BASE = '/home/ulrich/Documents/master2/projects/projet_covid/data/27-08_2020/'
AGGREG=BASE+'/aggreg/'
OUTPUT = AGGREG+"agg_data_per_days.csv"
INPUT = BASE+'donnees-hospitalieres-nouveaux-covid19-2020-08-27-19h00.csv'

df= pd.read_csv(INPUT, sep=';')
result_df = pd.DataFrame(columns=['jour', 'incid_hosp', 'incid_rea', 'incid_dc', 'incid_rad'])
df_days = df[['jour', 'incid_hosp', 'incid_rea', 'incid_dc', 'incid_rad']]
for idx, data in df_days.groupby('jour'):
    rad = data['incid_rad'].sum()
    dc = data['incid_dc'].sum()
    hosp = data['incid_hosp'].sum()
    rea = data['incid_rea'].sum()
    jour = idx
    data_append = {result_df.columns[0]:jour, 
                   result_df.columns[1]:hosp,
                   result_df.columns[2]:rea,
                   result_df.columns[3]:dc,
                   result_df.columns[4]:rad
                  }
    append_df = pd.DataFrame(data=[data_append])
    result_df = pd.concat([result_df, append_df], sort=False)
result_df.sort_values('jour').to_csv(OUTPUT, index=False)




