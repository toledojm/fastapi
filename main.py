from sqlalchemy.types import *
from fastapi import FastAPI
import crud

app = FastAPI()

# se crea la url de bienvenida

@app.get("/")
async def root():
    return {"message": "Ingrese.../Piloto....en la url para conocer el piloto con mayor cantidad de primeros puestos...../circuito....para conocer El circuito más recorrido...../pitoto_ganador....para conocer El piloto con mayor cantidad de puntos con constructor de ameriacano o britanico....../year......para conocer El año con más carreras"}

# se crea mediante el metodo get de fastAPI las querys del PI 01


# se crea el get de fastAPI  que devuelve el Piloto con mayor cantidad de primeros puestos

@app.get("/piloto/")
async def query():
    return crud.piloto()
   

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
   