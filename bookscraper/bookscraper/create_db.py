from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from orm import Base, engine

def create_database():
    # Créer toutes les tables définies dans Base.metadata
    Base.metadata.create_all(bind=engine)
    print("Base de données créée avec succès.")

if __name__ == "__main__":
    create_database()