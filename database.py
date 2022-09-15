from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import *

# se realiza la conexion a base de datos jwsDB MySQL

SQLALCHEMY_DATABASE_URL = "mysql://c3zpbaqh6klc7gdq:o0x2p2l6asmydogd@cwe1u6tjijexv3r6.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/wwhlk06iufgyn4ua"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

# se ingesta los datos a tablas a un database de jwsDB MySQL
# se crea claves primarias y foraneas para relacionar las tablas creadas

with engine.connect() as con, con.begin():
    df_circuits.to_sql('circuit', con, if_exists='replace', index=False)
    df_constructors.to_sql('constructor', con, if_exists='replace', index=False)
    df_drivers.to_sql('driver', con, if_exists='replace', index=False)
    df_results.to_sql('result', con, if_exists='replace', index=False)
    df_races.to_sql('race', con, if_exists='replace', index=False)
    con.execute('''ALTER TABLE circuit ADD PRIMARY KEY(circuitId);''')
    con.execute('''ALTER TABLE constructor ADD PRIMARY KEY(constructorId);''')
    con.execute('''ALTER TABLE driver ADD PRIMARY KEY(driverId);''')
    con.execute('''ALTER TABLE result ADD PRIMARY KEY(resultId);''')
    con.execute('''ALTER TABLE race ADD PRIMARY KEY(raceId);''')
    con.execute('''ALTER TABLE race ADD foreign key (circuitId) references circuit(circuitId);''')
    con.execute('''ALTER TABLE result ADD foreign key (raceId) references race(raceId);''')
    con.execute('''ALTER TABLE result ADD foreign key (driverId) references driver(driverId);''')
    con.execute('''ALTER TABLE result ADD foreign key (constructorId) references constructor(constructorId);''')
 