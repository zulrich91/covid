import requests
from bs4 import BeautifulSoup 
import requests 
from datetime import datetime
import os

FILES_NAME = ["donnees-hospitalieres-covid19-2020-08-31-19h00.csv",
             "donnees-hospitalieres-nouveaux-covid19-2020-08-31-19h00.csv",
             "donnees-hospitalieres-classe-age-covid19-2020-08-31-19h00.csv",
             "donnees-hospitalieres-etablissements-covid19-2020-08-31-19h00.csv",
              "metadonnees-donnees-hospitalieres-covid19.csv",
              "metadonnees-donnees-hospitalieres-covid19-nouveaux.csv",
              "metadonnees-donnees-hospitalieres-covid19-classes-age.csv",
              "metadonnees-services-hospitaliers-covid19.csv",
              "metadonnees-sexe.csv"]

MAPPING_FILE = "departements-france.csv"
AGG_FILE = "open_stats_coronavirus.csv"  

# Download the first 9 COVID 19 csv files present on the web data.gouv.fr 
page = requests.get("https://www.data.gouv.fr/fr/datasets/donnees-hospitalieres-relatives-a-lepidemie-de-covid-19/") 
soup = BeautifulSoup(page.content) 
links = soup.findAll("a")
downloads = []
today = datetime.now()

# Create a folder named as the date of the day
os.mkdir("flux_data/" + today.strftime('%Y%m%d')) 

# Extract the link to the csv files
for link in links: 
    if 'Télécharger' in link:
        downloads.append(link['href'])
# Download the csv files
for DOWNLOAD_PATH, DOWNLOAD_URL in zip(FILES_NAME,downloads[:9]):
    urllib.request.urlretrieve(DOWNLOAD_URL,"flux_data/" + today.strftime('%Y%m%d')+"/"+DOWNLOAD_PATH)

# Download the csv file containing the mapping of regions to their appropriate code numbers
page = requests.get("https://www.data.gouv.fr/fr/datasets/departements-de-france/?fbclid=IwAR3en1smTJleFB63SBcOZaZ_-KSMm__IR0DjCvrlA5qrnDpoMulyz8OvNCs#_") 
soup = BeautifulSoup(page.content) 
links = soup.findAll("a") 
mapping = []
for link in links: 
    if 'Télécharger' in link:
        mapping.append(link['href'])
urllib.request.urlretrieve(mapping[0],"flux_data/" + today.strftime('%Y%m%d')+"/"+MAPPING_FILE)


# Download the csv file containing daily aggregration of COVID data.
page = requests.get("https://www.coronavirus-statistiques.com/open-data/?fbclid=IwAR348zxIXqsjHviVo7XvIvHPuhgyEx5c1ztSUPlScGq1AYxDhSyZAjDZVYE") 
soup = BeautifulSoup(page.content) 
links = soup.findAll("a") 
agg = []
for link in links: 
    if 'Données brutes CSV' in link:
        agg.append(link['href'])
urllib.request.urlretrieve(agg[0],"flux_data/" + today.strftime('%Y%m%d')+"/"+AGG_FILE)











