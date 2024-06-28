from sqlalchemy.orm import Session
from models import Book
from orm import session

def filtre_par_titre(session, mot):
    x = 0
    for book in session.query(Book).filter(Book.Book_Title == mot).all():
        #print(book)
        x += 1
    print(f"Nombre total de livres trouvés pour le titre '{mot}': {x}")

def filtre_par_annee(session, annee):
    x = 0
    for book in session.query(Book).filter(Book.Year_Of_Publication == annee).all():
        #print(book)
        x += 1
    print(f"Nombre total de livres trouvés pour l'année {annee}: {x}")

def filtre_par_auteur(session, auteur):
    x = 0
    for book in session.query(Book).filter(Book.Book_Author == auteur).all():
        print(book)
        x += 1
    print(f"Nombre total de livres trouvés pour l'auteur.ice' {auteur}: {x}")

# Exemples d'appels de fonctions
# filtre_par_titre(session, 'The Hobbit')
# filtre_par_annee(session, 2000)
# filtre_par_auteur(session, 'Alison Bechdel')
