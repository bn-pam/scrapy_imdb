from sqlalchemy import Column, Integer, String, Float, Time, ForeignKey
from sqlalchemy.orm import declarative_base, relationship
from dotenv import load_dotenv
import os

load_dotenv()
Base = declarative_base()
# Définir la connexion à la base de données

# url de la BDD
DATABASE_URL = os.getenv("DATABASE_URL") 

class Films(Base):
    __tablename__ = 'films'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, nullable=True)
    scorepresse = Column(Float, nullable=True)
    scorespectateurs = Column(Float, nullable=True)
    annee = Column(String, nullable=True) 
    duree = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    boxofficefr = Column(Integer, nullable=True)

    #### relations films
    # realisateur_links = relationship('RealisateursLinkFilms', back_populates='films')
    realisateurs = relationship('Realisateurs', secondary='realisateurslinkfilms', back_populates='films')
    # acteur_links = relationship('ActeursLinkFilms', back_populates='films')
    acteurs = relationship('Acteurs', secondary='acteurslinkfilms', back_populates='films')
    # genre_links = relationship('GenreLinkFilms', back_populates='films')
    genres = relationship('Genre', secondary='genrelinkfilms', back_populates='films')
    # pays_links = relationship('PaysLinkFilms', back_populates='films')
    pays = relationship('Pays', secondary='payslinkfilms', back_populates='films')

    def __repr__(self):
        return f"<Films(id='{self.id}', titre='{self.titre}', realisateurs='{self.realisateurs}', annee='{self.annee}')>"
    
class Series(Base):
    __tablename__ = 'series'
    id = Column(Integer, primary_key=True, autoincrement=True)
    titre = Column(String, unique=True, nullable=True)
    scorepresse = Column(Float, nullable=True)
    scorespectateurs = Column(Float, nullable=True)
    annee = Column(String, nullable=True) 
    duree = Column(Integer, nullable=True)
    description = Column(String, nullable=True)
    saisons = Column(Integer, nullable=True)
    episodes = Column(Integer, nullable=True)

    #### relations series
    # realisateur_links = relationship('RealisateursLinkSeries', back_populates='series')
    realisateurs = relationship('Realisateurs', secondary='realisateurslinkseries', back_populates='series')
    # acteur_links = relationship('ActeursLinkSeries', back_populates='series')
    acteurs = relationship('Acteurs', secondary='acteurslinkseries', back_populates='series')
    # genre_links = relationship('GenreLinkSeries', back_populates='series')
    genres = relationship('Genre', secondary='genrelinkseries', back_populates='series')
    # pays_links = relationship('PaysLinkSeries', back_populates='series')
    pays = relationship('Pays', secondary='payslinkseries', back_populates='series')

    def __repr__(self):
        return f"<Series(id='{self.id}', titre='{self.titre}', realisateurs='{self.realisateurs}', annee='{self.annee}')>"
    
class Realisateurs(Base):
    __tablename__ = 'realisateurs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    realisateurs = Column(String, nullable=False)
    # film_links = relationship('RealisateursLinkFilms', back_populates='realisateurs')
    # serie_links = relationship('RealisateursLinkSeries', back_populates='realisateurs')
    films = relationship('Films', secondary='realisateurslinkfilms', back_populates='realisateurs')
    series = relationship('Series', secondary='realisateurslinkseries', back_populates='realisateurs')

class RealisateursLinkFilms(Base):
    __tablename__ = 'realisateurslinkfilms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id'), autoincrement=True)
    id_realisateur = Column(Integer, ForeignKey('realisateurs.id'), autoincrement=True)
    # films = relationship('Films', back_populates='realisateur_links')
    # realisateurs = relationship('Realisateurs', back_populates='film_links')


class RealisateursLinkSeries(Base):
    __tablename__ = 'realisateurslinkseries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_serie = Column(Integer, ForeignKey('series.id'), autoincrement=True)
    id_realisateur = Column(Integer, ForeignKey('realisateurs.id'), autoincrement=True)
    # series = relationship('Series', back_populates='realisateur_links')
    # realisateurs = relationship('Realisateurs', back_populates='serie_links')
    
class Acteurs(Base):
    __tablename__ = 'acteurs'
    id = Column(Integer, primary_key=True, autoincrement=True)
    acteurs = Column(String, nullable=False)
    # film_links = relationship('ActeursLinkFilms', back_populates='acteurs')
    # serie_links = relationship('ActeursLinkSeries', back_populates='acteurs')
    films = relationship('Films', secondary='acteurslinkfilms', back_populates='acteurs')
    series = relationship('Series', secondary='acteurslinkseries', back_populates='acteurs')


class ActeursLinkFilms(Base):
    __tablename__ = 'acteurslinkfilms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id'), autoincrement=True)
    id_acteur = Column(Integer, ForeignKey('acteurs.id'), autoincrement=True)
    # films = relationship('Films', back_populates='acteur_links')
    # acteurs = relationship('Acteurs', back_populates='serie_links')


class ActeursLinkSeries(Base):
    __tablename__ = 'acteurslinkseries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('series.id'), autoincrement=True)
    id_acteur = Column(Integer, ForeignKey('acteurs.id'), autoincrement=True)
    # series = relationship('Series', back_populates='acteur_links')
    # acteurs = relationship('Acteurs', back_populates='film_links')


class Genre(Base):
    __tablename__ = 'genre'
    id = Column(Integer, primary_key=True, autoincrement=True)
    genre = Column(String, nullable=False)
    # film_links = relationship('GenreLinkFilms', back_populates='genres')
    # serie_links = relationship('GenreLinkSeries', back_populates='genres')
    films = relationship('Films', secondary='genrelinkfilms', back_populates='genres')
    series = relationship('Series', secondary='genrelinkseries', back_populates='genres')


class GenreLinkFilms(Base):
    __tablename__ = 'genrelinkfilms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id'), autoincrement=True)
    id_genre = Column(Integer, ForeignKey('genre.id'), autoincrement=True)
    # films = relationship('Films', back_populates='genre_links')
    # genres = relationship('Genre', back_populates='film_links')


class GenreLinkSeries(Base):
    __tablename__ = 'genrelinkseries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_serie = Column(Integer, ForeignKey('series.id'), autoincrement=True)
    id_genre = Column(Integer, ForeignKey('genre.id'), autoincrement=True)
    # series = relationship('Series', back_populates='genre_links')
    # genres = relationship('Genre', back_populates='serie_links')


class Pays(Base):
    __tablename__ = 'pays'
    id = Column(Integer, primary_key=True, autoincrement=True)
    pays = Column(String, nullable=False)
    # film_links = relationship('PaysLinkFilms', back_populates='pays')
    # serie_links = relationship('PaysLinkSeries', back_populates='pays')
    films = relationship('Films', secondary='payslinkfilms', back_populates='pays')
    series = relationship('Series', secondary='payslinkseries', back_populates='pays')

class PaysLinkFilms(Base):
    __tablename__ = 'payslinkfilms'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_film = Column(Integer, ForeignKey('films.id'), autoincrement=True)
    id_pays = Column(Integer, ForeignKey('pays.id'), autoincrement=True)
    # films = relationship('Films', back_populates='pays_links')
    # pays = relationship('Pays', back_populates='film_links')


class PaysLinkSeries(Base):
    __tablename__ = 'payslinkseries'
    id = Column(Integer, primary_key=True, autoincrement=True)
    id_serie = Column(Integer, ForeignKey('series.id'), autoincrement=True)
    id_pays = Column(Integer, ForeignKey('pays.id'), autoincrement=True)
    # series = relationship('Series', back_populates='pays_links')
    # pays = relationship('Pays', back_populates='serie_links')



    # @classmethod
    # def ajouter_livre(cls, session, ISBN, title, auteur, annee, editeur, img_url_s, img_url_m, img_url_l):
    #     nouveau_livre = cls(ISBN=ISBN, Book_Title=title, Book_Author=auteur, Year_Of_Publication=annee, Publisher=editeur, Image_URL_S= img_url_s, Image_URL_M= img_url_m, Image_URL_L= img_url_l)
    #     session.add(nouveau_livre)
    #     session.commit()
    #     print(f"Livre ajouté : {nouveau_livre}")
