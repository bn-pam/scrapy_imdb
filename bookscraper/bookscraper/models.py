from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from orm import Base

Base = declarative_base()
DATABASE_URL = ''

class Films(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=False)
    scorepresse = Column(float, nullable=False)
    scorespectateurs = Column(float, nullable=False)
    genres = Column(Integer, nullable=False)
    annee = Column(String, nullable=False) 
    duree = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    boxoffice = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Films(id='{self.id}', titre='{self.titre}', realisateurs='{self.realisateurs}', annee='{self.annee}')>"
    
class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, unique=True, nullable=False)
    scorepresse = Column(float, nullable=False)
    scorespectateurs = Column(float, nullable=False)
    genres = Column(Integer, nullable=False)
    annee = Column(String, nullable=False) 
    duree = Column(Integer, nullable=False)
    description = Column(String, nullable=False)
    saisons = Column(Integer, nullable=False)
    episodes = Column(Integer, nullable=False)
    
    def __repr__(self):
        return f"<Series(id='{self.id}', titre='{self.titre}', realisateurs='{self.realisateurs}', annee='{self.annee}')>"
    
class Realisateurs(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    realisateur = Column(String, nullable=False)

class RealisateursLinkFilms(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id'), autoincrement=True)
    id_realisateur = Column(Integer, ForeignKey('realisateurs.id'), autoincrement=True)

class RealisateursLinkSeries(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_serie = Column(Integer, ForeignKey('series.id'), autoincrement=True)
    id_realisateur = Column(Integer, ForeignKey('realisateurs.id'), autoincrement=True)
    
class Acteurs(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    acteur = Column(String, nullable=False)

class ActeursLinkFilms(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id'), autoincrement=True)
    id_acteur = Column(Integer, ForeignKey('acteurs.id'), autoincrement=True)

class ActeursLinkSeries(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('series.id'), autoincrement=True)
    id_acteur = Column(Integer, ForeignKey('acteurs.id'), autoincrement=True)

class Genre(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String, nullable=False)

class GenreLinkFilms(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id'), autoincrement=True)
    id_pays = Column(Integer, ForeignKey('genre.id'), autoincrement=True)

class GenreLinkSeries(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_serie = Column(Integer, ForeignKey('series.id'), autoincrement=True)
    id_genre = Column(Integer, ForeignKey('genres.id'), autoincrement=True)

class Pays(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    pays = Column(String, nullable=False)

class PaysLinkFilms(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id'), autoincrement=True)
    id_pays = Column(Integer, ForeignKey('pays.id'), autoincrement=True)

class PayssLinkSeries(Base):
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_serie = Column(Integer, ForeignKey('series.id'), autoincrement=True)
    id_pays = Column(Integer, ForeignKey('pays.id'), autoincrement=True)


    # @classmethod
    # def ajouter_livre(cls, session, ISBN, title, auteur, annee, editeur, img_url_s, img_url_m, img_url_l):
    #     nouveau_livre = cls(ISBN=ISBN, Book_Title=title, Book_Author=auteur, Year_Of_Publication=annee, Publisher=editeur, Image_URL_S= img_url_s, Image_URL_M= img_url_m, Image_URL_L= img_url_l)
    #     session.add(nouveau_livre)
    #     session.commit()
    #     print(f"Livre ajouté : {nouveau_livre}")
