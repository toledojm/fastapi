from sqlalchemy.types import *
import pandas as pd
import urllib.request
import ssl


# se crea la ingesta de los datasets desde el repo de github forkeado PI01_DATA03

# se crea las url correspondientes a cada dataset de interes

ssl._create_default_https_context = ssl._create_unverified_context
circuits = urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/circuits.csv')
constructors= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/constructors.json')
results= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/results.json')
drivers= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/drivers.json')
races= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/races.csv')

# se crea los dataframes

df_circuits= pd.read_csv(circuits)
df_constructors= pd.read_json(constructors,lines=True)
df_results= pd.read_json(results,lines=True)
df_drivers= pd.read_json(drivers,lines=True)
df_races= pd.read_csv(races)

# se normaliza los dataframes

df_constructors.drop('url', axis=1, inplace=True)
df_circuits.drop(['lat','lng','alt','url','circuitRef'], axis=1, inplace=True)
df_drivers=pd.concat([df_drivers,pd.json_normalize(df_drivers.name, max_level=1)],axis=1)
df_races.drop(['url','time','date'], axis=1, inplace=True)
df_drivers.drop(['name','url','dob','code','number'], axis=1, inplace=True)
df_results.drop(['fastestLapTime','time','milliseconds','fastestLapSpeed','fastestLap','grid','positionText'], axis=1, inplace=True)
df_races['year']=df_races.year.astype(str)

# se ingesta los datos a tablas a un database de jwsDB MySQL
# se crea claves primarias y foraneas para relacionar las tablas creadas

