# Proyecto Individual 1- Data 03- Soy Henry
# José María Toledo
## Creación de una API


## Consigna
Para este proyecto individual, se creo y ejecuto de una API mediante el framework de FastAPI y el deploy en Heroku.

## Ejecución
Se crearon los scripts correspondientes en phyton para:
1. realizar la ingesta y normalización de los datasets del repositorio de github forkeado ubicado en https://github.com/FnegreteHenry/PI01_DATA03
2. crear la conexion a base de datos jwsDB MySQL
3. crear, instanciar y realizar las query's nesesarias para responder las preguntas de PI en el framework de FastAPI
4. realizar el deploy en Heroku https://josetoledo-data03-dsh-fastappi.herokuapp.com/
- Año con más carreras https://josetoledo-data03-dsh-fastappi.herokuapp.com/year/
- Piloto con mayor cantidad de primeros puestos https://josetoledo-data03-dsh-fastappi.herokuapp.com/piloto/
- Nombre del circuito más corrido https://josetoledo-data03-dsh-fastappi.herokuapp.com/circuito/
- Piloto con mayor cantidad de puntos en total, cuyo constructor sea de nacionalidad sea American o British https://josetoledo-data03-dsh-fastappi.herokuapp.com/piloto_ganador


  
## Descripción de los Scrpits/modulos en un repositorio de github https://github.com/toledojm/fastapi
.
└── fastappi
    ├── __init_.py ->se empaqueta los modulos dentro de la carpeta fastappi
    ├── crud.py -> se crean las funciones con las query's para interactuar con el database
    ├── database.py ->se crea la conexión mediante sqlalchemy al database de jwsDB MySQL
    ├── main.py ->se integran y usan todos modulos con el framework de FastAPI
    ├── models.py --se realiza la ingesta y normalización de los datasets



