from sqlalchemy.types import *
from fastapi import FastAPI
import pandas as pd
from database import SessionLocal, engine
import crud
from sqlalchemy.orm import Session

Session=SessionLocal()

app = FastAPI()

# se crea la url de bienvenida

@app.get("/")
async def root():
    return {"message": "Ingrese.../piloto....en la url para conocer el piloto con mayor cantidad de primeros puestos...../circuito....para conocer El circuito más recorrido...../pitoto_ganador....para conocer El piloto con mayor cantidad de puntos con constructor de ameriacano o britanico....../year......para conocer El año con más carreras"}

# se crea mediante el metodo get de fastAPI las querys del PI 01


# se crea el get de fastAPI  que devuelve el Piloto con mayor cantidad de primeros puestos

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
   

# se crea el get de fastAPI que devuelve el circuito más recorrido

@app.get("/circuito/")
async def query():
    return crud.circuito()
   

# se crea el get de fastAPI que devuelve el piloto más ganador 
# con constructor americano o britanico

@app.get("/piloto_ganador/")
async def query():
    return crud.piloto_ganador()
    
# se crea el get de fastAPI que devuelve el año con mas carreras

@app.get("/year/")
async def query():
    return crud.year()
   