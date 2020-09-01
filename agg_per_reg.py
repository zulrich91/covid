import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt
from scipy.integrate import odeint


BASE = '/home/ulrich/Documents/master2/projects/projet_covid/data/27-08_2020/'
INPUT = BASE+'donnees-hospitalieres-classe-age-covid19-2020-08-27-19h00.csv'
AGGREG=BASE+'/aggreg/'
OUTPUT = AGGREG+'agg_data_per_regions.csv'
regions_dict = {1:"Guadeloupe",2:"Martinique",3:"Guyane",4:"La Réunion",
				6:"Mayotte",11:"Île-de-France",24:"Centre-Val de Loire",
				27:"Bourgogne-Franche-Comté",28:"Normandie",32:"Hauts-de-France",
				44:"Grand Est",52:"Pays de la Loire",53:"Bretagne",75:"Nouvelle-Aquitaine",
				76:"Occitanie",84:"Auvergne-Rhône-Alpes",93:"Provence-Alpes-Côte d'Azur", 
				94:"Corse"}

df = pd.read_csv(INPUT, sep=';', header=0)
df_reg = df[['reg', 'jour','hosp', 'rea', 'rad','dc']]
result_df = pd.DataFrame(columns=['reg','hosp', 'rea', 'rad','dc'])
for idx, data in df_reg.groupby('reg'):
    rad = data['rad'].max()
    dc = data['dc'].max()
    hosp = data['hosp'].sum()
    rea = data['rea'].sum()
    reg = regions_dict[idx]
    data_append = {result_df.columns[0]:reg, 
                   result_df.columns[1]:hosp,
                   result_df.columns[2]:rea,
                   result_df.columns[3]:rad,
                   result_df.columns[4]:dc
                  }
    append_df = pd.DataFrame(data=[data_append])
    result_df = pd.concat([result_df, append_df], sort=False)

result_df.to_csv(OUTPUT,index=False)