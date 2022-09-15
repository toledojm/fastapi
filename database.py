from sqlalchemy import create_engine

# se realiza la conexion a base de datos jwsDB MySQL



SQLALCHEMY_DATABASE_URL = "mysql://mngkf00q4w3oljo0:t9z9i932syo45knv@cwe1u6tjijexv3r6.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/w8vs956ehcksvjqu"
SQLALCHEMY_DATABASE_URL1="mysql+pymysql://root:toledin1@localhost/db"
engine = create_engine(SQLALCHEMY_DATABASE_URL1)

engine.connect()