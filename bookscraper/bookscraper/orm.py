from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
# from dotenv import load_dotenv
import os

# load_dotenv()

# Définir la connexion à la base de données

# url de la BDD
DATABASE_URL = ""
#os.getenv("DATABASE_URL") 

# créer une instance du moteur SQLAlchemy
engine = create_engine(DATABASE_URL) 

# Créer une factory de sessions SQLAlchemy (générateur de sessions)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Déclarer une base pour que les modèles la partagent
Base = declarative_base()

#créer une session à partir du générateur de sessions
session=SessionLocal()