from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from models import *

# se realiza la conexion a base de datos jwsDB MySQL

SQLALCHEMY_DATABASE_URL = "mysql://prs679z1zrvo3g14:g51vxn3imv6mx9i6@cwe1u6tjijexv3r6.cbetxkdyhwsb.us-east-1.rds.amazonaws.com:3306/hp3gqgswj6ocf8l3"

engine = create_engine(SQLALCHEMY_DATABASE_URL)

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
 