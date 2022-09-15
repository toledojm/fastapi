import pandas as pd
from main import engine

engine.connect()
# se crea la función con la query que devuelve el Piloto con mayor cantidad de primeros puestos

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

# se crea la función con la query que devuelve el circuito más recorrido

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
    return {"El circuito más recorrido es:": circuito}

# se crea la función con la query que devuelve el piloto más ganador 
# con constructor americano o britanico

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

# se crea la función con la query que devuelve el año con mas carreras

async def year():
    query_year ='''select year ,count(raceId) as carreras
                    from race
                    group by year
                    order by carreras DESC
                    LIMIT 1;'''
    df = pd.read_sql(query_year, engine)
    year=df.iloc[0]['year']
    return {"El año con más carreras es:": year}