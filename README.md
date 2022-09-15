# Proyecto Individual 1- Data 03- Soy Henry
## José María Toledo

### Consigna: Creación de una API

Para este proyecto individual, se creo y ejecuto una API mediante el framework de FastAPI y el deploy en Heroku utilizando jawsDB MySQL y github

![](https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Heroku_logo.svg/320px-Heroku_logo.svg.png)
![](https://upload.wikimedia.org/wikiversity/en/thumb/8/8c/FastAPI_logo.png/320px-FastAPI_logo.png)
![](https://pngimg.com/uploads/github/github_PNG37.png)
![](https://res.cloudinary.com/crunchbase-production/image/upload/c_lpad,h_170,w_170,f_auto,b_white,q_auto:eco,dpr_1/chmyinpr1ffsc0jvpil2)



### Ejecución

Se crearon los scripts/moldulos correspondientes en un repositorio de github para:
1. realizar la ingesta y normalización de los datasets del repositorio de github forkeado https://github.com/FnegreteHenry/PI01_DATA03
2. crear la conexion a base de datos jawsDB MySQL
3. crear, instanciar y realizar las query's nesesarias para responder las preguntas de PI en el framework de FastAPI
4. realizar el deploy en Heroku https://josetoledo-dhs-fastapi.herokuapp.com/
- Año con más carreras https://josetoledo-dhs-fastapi.herokuapp.com/year/
- Piloto con mayor cantidad de primeros puestos https://josetoledo-dhs-fastapi.herokuapp.com/piloto/
- Nombre del circuito más corrido https://josetoledo-dhs-fastapi.herokuapp.com/circuito/
- Piloto con mayor cantidad de puntos en total, cuyo constructor sea de nacionalidad sea American o British https://josetoledo-dhs-fastapi.herokuapp.com/piloto_ganador/


  
### Descripción de los Scrpits/modulos del repositorio de github utilizados para el deploy en Heroku.

dentro de la carpeta fastappi se crean los modulos:
- *database.py* ->se crea la conexión mediante sqlalchemy al database de jawsDB MySQL y se crean las funciones con las query's para interactuar con el database
- *main.py*->se integran y usan todos modulos con el framework de FastAPI
- *models.py*->se realiza la ingesta y normalización de los datasets
- *requirements.txt*->modulos externos a phyton para correr el el deploy en Heroku
- *Procfile*-> contiene la sentencia de *uvicorn* para correr el framework de FastAPI





