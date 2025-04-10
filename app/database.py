from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Definir la URL de la base de datos
SQLALCHEMY_DATABASE_URL = "mysql+mysqlconnector://root:232041@localhost/notepad_db"

# Crear el motor de la base de datos
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={})

# Crear la sesión de la base de datos
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Definir la base para las clases del modelo
Base = declarative_base()
