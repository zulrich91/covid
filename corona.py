import pandas as pd

# Data source : https://www.coronavirus-statistiques.com/open-data/?fbclid=IwAR0Mn7mZqd1zh3Dz54wL8CViwDSJDSHSkiU1lxwxr2dRvVQCkIme49WVZdc
corona = pd.read_csv("/home/ulrich/Documents/master2/projects/projet_covid/data/open_stats_coronavirus.csv", sep=";")
corona_fr = corona[corona['nom']=='france']
corona_fr.to_csv('/data/corona_virus.csv', index=False)