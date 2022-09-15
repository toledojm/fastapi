from sqlalchemy import create_engine
from sqlalchemy.types import *
import pandas as pd
import urllib.request
from fastapi import FastAPI
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

# se realiza la conexion a base de datos jwsDB MySQL

URL = "mysql://mngkf00q4w3oljo0:t9z9i932syo45knv@cwe1u6tjijexv3r6.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/w8vs956ehcksvjqu"
engine = create_engine(URL)

# se ingesta los datos a tablas a un database de jwsDB MySQL
# se crea claves primarias y foraneas para relacionar las tablas creadas

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
 

# se instancia a fastAPI

app = FastAPI()

# se crea la url de bienvenida

@app.get("/")
async def root():
    return {"message": "Ingrese.../Piloto....en la url para conocer el piloto con mayor cantidad de primeros puestos...../circuito....para conocer El circuito más recorrido...../pitoto_ganador....para conocer El piloto con mayor cantidad de puntos con constructor de ameriacano o britanico....../year......para conocer El año con más carreras"}

# se crea mediante el metodo get de fastAPI las querys del PI 01


# se crea la query que devuelve el Piloto con mayor cantidad de primeros puestos

@app.get("/piloto/")
async def piloto():
    query_piloto ='''SELECT DISTINCT d.driverRef as piloto, count(d.driverRef) as primerpuesto 
                        FROM driver d JOIN result r 
                        ON (d.driverId=r.driverId) AND r.position=1
                        GROUP BY d.driverRef
                        ORDER BY primerpuesto DESC
                        LIMIT 1;'''
    df = pd.read_sql(query_piloto, engine)
    piloto=df.iloc[0]['piloto']
    return {"El Piloto con mayor cantidad de primeros puestos es:": piloto}

#se crea la query que devuelve el circuito más recorrido

@app.get("/circuito/")
async def citcuito():
    query_circuito ='''select distinct c.name as circuito, count(r.circuitId) as CircuitoMasRecorrido
                        from circuit c
                        join race r
                        on r.circuitId=c.circuitId
                        group by c.name
                        order by CircuitoMasRecorrido DESC
                        LIMIT 1;'''
    df = pd.read_sql(query_circuito, engine)
    circuito=df.iloc[0]['circuito']
    return {"El circuito más recorrido es:": circuito}

# se crea la query que devuelve el piloto más ganador 
# con constructor americano o britanico

@app.get("/piloto_ganador/")
async def piloto_ganador():
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

# se crea la query que devuelve el año con mas carreras

@app.get("/year/")
async def year():
    query_year ='''select year ,count(raceId) as carreras
                    from race
                    group by year
                    order by carreras DESC
                    LIMIT 1;'''
    df = pd.read_sql(query_year, engine)
    year=df.iloc[0]['year']
    return {"El año con más carreras es:": year}