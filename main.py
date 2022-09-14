from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import urllib.request
import ssl
from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationships
from fastapi import FastAPI
import pymysql
pymysql.install_as_MySQLdb()



ssl._create_default_https_context = ssl._create_unverified_context
circuits = urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/circuits.csv')
constructors= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/constructors.json')
results= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/results.json')
drivers= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/drivers.json')
races= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/races.csv')

df_circuits= pd.read_csv(circuits)
df_constructors= pd.read_json(constructors,lines=True)
df_results= pd.read_json(results,lines=True)
df_drivers= pd.read_json(drivers,lines=True)
df_races= pd.read_csv(races)

df_constructors.drop('url', axis=1, inplace=True)
df_circuits.drop(['lat','lng','alt','url','circuitRef'], axis=1, inplace=True)
df_drivers=pd.concat([df_drivers,pd.json_normalize(df_drivers.name, max_level=1)],axis=1)
df_races.drop(['url','time','date'], axis=1, inplace=True)
df_drivers.drop(['name','url','dob','code','number'], axis=1, inplace=True)
df_results.drop(['position','fastestLapTime','time','milliseconds','fastestLapSpeed','fastestLap','grid','positionText'], axis=1, inplace=True)


SQLALCHEMY_DATABASE_URL = "mysql+mysqldb://root:toledin1@localhost/db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

with engine.connect() as conn, conn.begin():
    df_circuits.to_sql('circuit', conn, if_exists='append', index=False)
    df_constructors.to_sql('constructor', conn, if_exists='append', index=False)
    df_drivers.to_sql('driver', conn, if_exists='append', index=False)
    df_results.to_sql('result', conn, if_exists='append', index=False)
    df_races.to_sql('race', conn, if_exists='append', index=False)

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Ingrese /Piloto en la url para conocer el piloto con mayor cantidad de primeros puestos"}


@app.get("/Piloto/")
async def driver():
    query2 ='''select d.surname as Apellido, count(r.positionOrder) as CantVictorias
    from driver d
    join result r
    on (r.driverId = d.driverId)
    where r.positionOrder = 1
    group by d.surname
    order by CantVictorias DESC
    LIMIT 1'''
    df = pd.read_sql(query2, engine)
    nombre=df['Apellido']
    return {"El Piloto con mayor cantidad de primeros puestos es:": nombre}

