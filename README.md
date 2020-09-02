# covid
* The code base of the Covid project at ILIS 
* The dash application is hosted at URL https://covid-tchuenkam.herokuapp.com/
* `agg_per_day.py`: Script to aggregate the data on daily basis.
* `agg_per_reg.py`: Script to aggregate the data at the regional level. 
* `app.py`: Script running the dashboard.
* `clean_preval.py`: Script to clean the dataset of indicators.
* `flux.py`: Script to automatically download data from the various sources.
* `google_mobility.py`: Script to preprocess google mobility to extract data about France. 
* `sir_per_day.py`: Script to preprocess data and extract a SIR model ready dataset. 
* `corona.py` : Script to extract France's aggregated hospital data form the datasets of [Corona Virus Statistique](https://www.coronavirus-statistiques.com/open-data/?fbclid=IwAR0Mn7mZqd1zh3Dz54wL8CViwDSJDSHSkiU1lxwxr2dRvVQCkIme49WVZdc).
* `requirements.txt`: Packages required to run the dashboard.
* `Ulrich TCHUENKAM_ Covid Project (2).pdf`: Project report. 

# Host project
* The instructions on how to host the application are available [here](https://dash.plotly.com/deployment) on heroku 

# Data Sources
* [Santé Publique France: Hospital data](https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/)
* [Santé Publique France: GEODES (Geo Donnees en Sante Publique)](https://geodes.santepubliquefrance.fr/#c=indicator&view=map2)
* [Corona Virus Statistiques](https://www.coronavirus-statistiques.com/open-data/?fbclid=IwAR0Mn7mZqd1zh3Dz54wL8CViwDSJDSHSkiU1lxwxr2dRvVQCkIme49WVZdc)
* [Google Mobility](https://www.google.com/covid19/mobility/)
* [Code mapping of regions of France](https://www.data.gouv.fr/fr/datasets/departements-de-france/?fbclid=IwAR3en1smTJleFB63SBcOZaZ_-KSMm__IR0DjCvrlA5qrnDpoMulyz8OvNCs#_)
* [Donnees Estimation de la population de la population francaise au 1ᵉʳ janvier 2020](https://www.insee.fr/fr/statistiques/1893198)
