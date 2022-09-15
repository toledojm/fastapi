from sqlalchemy.types import *
from fastapi import FastAPI
import pandas as pd
from database import engine
import crud 

app = FastAPI()

# se crea la url de bienvenida

@app.get("/")
async def root():
    return {"message": "añadir a la dirrecion URL:/piloto/->para conocer el piloto con mayor cantidad de primeros puestos,/circuito/->para conocer El circuito más recorrido,/piloto_ganador/->para conocer El piloto con mayor cantidad de puntos con constructor de ameriacano o britanico,/year/->para conocer el año con más carreras realizadas"}

# se crea mediante el metodo get de fastAPI las querys del PI 01


# se crea el get de fastAPI  que devuelve el Piloto con mayor cantidad de primeros puestos

@app.get("/piloto/")
async def piloto():
    query_piloto ='''SELECT DISTINCT d.driverRef as piloto, count(d.driverRef) as CantPrimerPuesto 
                        FROM driver d JOIN result r 
                        ON (d.driverId=r.driverId) AND r.position=1
                        GROUP BY d.driverRef
                        ORDER BY CantPrimerPuesto DESC
                        LIMIT 1;'''
    df = pd.read_sql(query_piloto, engine)
    piloto=df.iloc[0]['piloto']
    puesto=df.iloc[0]['CantPrimerPuesto']
    return {"El Piloto con mayor cantidad de primeros puestos es:": piloto,"con cantidad de primeros puestos:":puesto}
   

# se crea el get de fastAPI que devuelve el circuito más recorrido

@app.get("/circuito/")
async def circuito():
    query_circuito ='''select distinct c.name as circuito, count(r.circuitId) as CircuitoMasRecorrido
                        from circuit c
                        join race r
                        on r.circuitId=c.circuitId
                        group by c.name
                        order by CircuitoMasRecorrido DESC
                        LIMIT 1;'''
    df = pd.read_sql(query_circuito, engine)
    circuito=df.iloc[0]['circuito']
    recorrido=df.iloc[0]['CircuitoMasRecorrido']
    return {"El circuito más recorrido es:": circuito,"con recorridos totales:":recorrido}
   

# se crea el get de fastAPI que devuelve el piloto más ganador 
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
    puntos=df.iloc[0]['CantPuntosTotales']
    return {"El piloto con mayor cantidad de puntos con constructor de ameriacano o britanico es:": piloto,"con puntos totales:":puntos}
    
# se crea el get de fastAPI que devuelve el año con mas carreras

@app.get("/year/")
async def year():
    query_year ='''select year ,count(raceId) as CantCarreras
                    from race
                    group by year
                    order by carreras DESC
                    LIMIT 1;'''
    df = pd.read_sql(query_year, engine)
    year=df.iloc[0]['year']
    carrera=df.iloc[0]['CantCarreras']
    return {"El año con más carreras es:": year,"con cantidad de carreras:":carrera}
   