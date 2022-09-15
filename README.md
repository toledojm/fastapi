# Proyecto Individual 1- Data 03- Soy Henry
## José María Toledo

### Consigna: Creación de una API

Para este proyecto individual, se creo y ejecuto de una API mediante el framework de FastAPI y el deploy en Heroku utilizando jawsDB MySQL y github

<img src="https://upload.wikimedia.org/wikipedia/commons/e/ec/Heroku_logo.svg" align="left" height="200" width="200" ></a>


### Ejecución

Se crearon los scripts correspondientes en phyton para:
1. realizar la ingesta y normalización de los datasets del repositorio de github forkeado ubicado en https://github.com/FnegreteHenry/PI01_DATA03
2. crear la conexion a base de datos jawsDB MySQL
3. crear, instanciar y realizar las query's nesesarias para responder las preguntas de PI en el framework de FastAPI
4. realizar el deploy en Heroku https://josetoledo-dhs-fastapi.herokuapp.com/
- Año con más carreras https://josetoledo-dhs-fastapi.herokuapp.com/year/
- Piloto con mayor cantidad de primeros puestos https://josetoledo-dhs-fastapi.herokuapp.com/piloto/
- Nombre del circuito más corrido https://josetoledo-dhs-fastapi.herokuapp.com/circuito/
- Piloto con mayor cantidad de puntos en total, cuyo constructor sea de nacionalidad sea American o British https://josetoledo-dhs-fastapi.herokuapp.com/piloto_ganador/


  
### Descripción de los Scrpits/modulos del repositorio de github utilizados para el deploy en Heroku.

dentro de la carpeta fastappi se crean los modulos:
- *database.py* ->se crea la conexión mediante sqlalchemy al database de jwsDB MySQL y se crean las funciones con las query's para interactuar con el database
- *main.py*->se integran y usan todos modulos con el framework de FastAPI
- *models.py*->se realiza la ingesta y normalización de los datasets
- *requirements.txt*->modulos externos a phyton para correr el el deploy en Heroku
- *Procfile*-> contiene la sentencia de *uvicorn* para correr el framework de FastAPI





