from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import pandas as pd
import urllib.request
import ssl
from sqlalchemy.orm import relationships
from fastapi import FastAPI
from sqlalchemy.types import *


# busco los datos desde github

ssl._create_default_https_context = ssl._create_unverified_context
circuits = urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/circuits.csv')
constructors= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/constructors.json')
results= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/results.json')
drivers= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/drivers.json')
races= urllib.request.urlopen('https://raw.githubusercontent.com/toledojm/PI01_DATA03/main/Datasets/races.csv')

# levanto con pandas

df_circuits= pd.read_csv(circuits)
df_constructors= pd.read_json(constructors,lines=True)
df_results= pd.read_json(results,lines=True)
df_drivers= pd.read_json(drivers,lines=True)
df_races= pd.read_csv(races)

# normalizo los dataframes

df_constructors.drop('url', axis=1, inplace=True)
df_circuits.drop(['lat','lng','alt','url','circuitRef'], axis=1, inplace=True)
df_drivers=pd.concat([df_drivers,pd.json_normalize(df_drivers.name, max_level=1)],axis=1)
df_races.drop(['url','time','date'], axis=1, inplace=True)
df_drivers.drop(['name','url','dob','code','number','driverRef'], axis=1, inplace=True)
df_results.drop(['position','fastestLapTime','time','milliseconds','fastestLapSpeed','fastestLap','grid','positionText'], axis=1, inplace=True)
df_races['year']=df_races.year.astype(str)

# creo la conexion a slq

URL = "mysql://izlqvlc80sbd9gd1:seq72zceq6k61so7@cwe1u6tjijexv3r6.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/aor5pfo8ypqr2uvs"

engine = create_engine(URL)

# ingesto los datos a tablas de un database sql
# creo claves primarias y foraneas y relaciono las tablas

with engine.connect() as conn, conn.begin():
    df_circuits.to_sql('circuit', conn, if_exists='append', index=False)
    df_constructors.to_sql('constructor', conn, if_exists='append', index=False)
    df_drivers.to_sql('driver', conn, if_exists='append', index=False)
    df_results.to_sql('result', conn, if_exists='append', index=False)
    df_races.to_sql('race', conn, if_exists='append', index=False)
    conn.execute('''ALTER TABLE circuit ADD PRIMARY KEY(circuitId);''')
    conn.execute('''ALTER TABLE constructor ADD PRIMARY KEY(constructorId);''')
    conn.execute('''ALTER TABLE driver ADD PRIMARY KEY(driverId);''')
    conn.execute('''ALTER TABLE result ADD PRIMARY KEY(resultId);''')
    conn.execute('''ALTER TABLE race ADD PRIMARY KEY(raceId);''')
    conn.execute('''ALTER TABLE race ADD foreign key (circuitId) references circuit(circuitId);''')
    conn.execute('''ALTER TABLE result ADD foreign key (raceId) references race(raceId);''')
    conn.execute('''ALTER TABLE result ADD foreign key (driverId) references driver(driverId);''')
    conn.execute('''ALTER TABLE result ADD foreign key (constructorId) references constructor(constructorId);''')
 

# instancia fastapi

app = FastAPI()

# creo url de bienvenida

@app.get("/")
async def root():
    return {"message": "Ingrese /Piloto en la url para conocer el piloto con mayor cantidad de primeros puestos\nIngrese /circuito en la url para conocer El circuito más recorrido\nIngrese /pitoto_ganador en la url para conocer El piloto con mayor cantidad de puntos con constructor de ameriacano o britanico\nIngrese /year en la url para conocer El año con más carreras\n"}

# creo url con la query que muestre el Piloto con mayor cantidad de primeros puestos

@app.get("/piloto/")
async def piloto1():
    query_piloto ='''select d.surname as piloto, count(r.positionOrder) as CantVictorias
                        from driver d
                        join result r
                        on (r.driverId = d.driverId)
                        where r.positionOrder = 1
                        group by d.surname
                        order by CantVictorias DESC
                        LIMIT 1;'''
    df = pd.read_sql(query_piloto, engine)
    piloto=df.iloc[0]['piloto']
    return {"El Piloto con mayor cantidad de primeros puestos es:": piloto}

#creo url con la query con el circuito más recorrido

@app.get("/circuito/")
async def citcuito1():
    query_circuito ='''select name, count(circuitId) as CircuitoMasRecorrido
                    from race
                    group by name
                    order by CircuitoMasRecorrido DESC
                    LIMIT 1;'''
    df = pd.read_sql(query_circuito, engine)
    circuito=df.iloc[0]['name']
    return {"El circuito más recorrido es:": circuito}

# creo url con la query el piloto más ganador 
# con constructor americano o britanico

@app.get("/piloto_ganador/")
async def piloto2():
    query_piloto ='''select r.surname as piloto, sum(r.points) as CantPuntosTotales
                    from (select c.constructorId
                            from constructor c
                            where c.nationality in ('British','American')) as c
                    join (select r.driverId, d.surname,  r.constructorId, r.points
                            from driver d
                            join result r
                            on d.driverId = r.driverId) as r
                    on r.constructorId=c.constructorId
                    group by r.surname
                    order by CantPuntosTotales DESC
                    LIMIT 1;'''
    df = pd.read_sql(query_piloto, engine)
    piloto=df.iloc[0]['piloto']
    return {"El piloto con mayor cantidad de puntos con constructor de ameriacano o britanico es:": piloto}

@app.get("/year/")
async def year1():
    query_year ='''select year ,count(raceId) as carreras
                    from race
                    group by year
                    order by carreras DESC
                    LIMIT 1;'''
    df = pd.read_sql(query_year, engine)
    year=df.iloc[0]['year']
    return {"El año con más carreras es:": year}