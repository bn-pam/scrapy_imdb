# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlalchemy, psycopg2
import re, dateparser, datetime, attempt
import dotenv, os, time
from sqlalchemy.exc import OperationalError
from bookscraper.orm import SessionLocal
from bookscraper.orm import session
from bookscraper.models import Films, Series, Realisateurs, RealisateursLinkFilms, RealisateursLinkSeries, Acteurs, ActeursLinkFilms, ActeursLinkSeries, Genre, GenreLinkFilms, GenreLinkSeries, Pays, PaysLinkFilms, PaysLinkSeries

###########################################################################################################################################################
###########################################################################################################################################################

# PIPELINE FILMS :

###########################################################################################################################################################
###########################################################################################################################################################
class DatabasePipelineFilm :

    def open_spider(self, spider):
        # Se connecter à la base de données
        # Créer la table si elle n'existe pas
       
       ##### créer une connexion à la bdd postgre
        from bookscraper.orm import session
        self.session=session

    def process_item(self, item, spider):
        # Insérer les données dans la base de données :
        # - règle pour vérifier l'existence de l'entité dans la table correspondante
        # - ajout de l'entité

        #table films
        # try : 
        existing_film = self.session.query(Films).filter_by(titre=item['titre'], annee=item['annee']).first()
        if existing_film is not None :
            film=existing_film
        else : 
            film=Films(titre=item['titre'], scorepresse = item['scorepresse'], scorespectateurs = item['scorespectateurs'], annee = item['annee'], duree = item['duree'], description = item['description'], boxofficefr = item['boxofficefr'])
            self.session.add(film)
            session.commit()
        # except OperationalError as e:
        #     session.rollback()  # Rollback en cas d'erreur
        #     print(f"Tentative {attempt + 1} : Erreur lors de l'insertion des données : {e}")
        #     time.sleep(1)  # Pause avant de réessayer
        # finally:
        #     session.close()  # Fermer la session SQLAlchemy

        #table realisateurs
        if isinstance(item['realisateur'], list): # vérifier que l'élement est une liste
            for scrap_realisateur in item['realisateur']: #savoir si dans la liste de real scrappée
                existing_real = self.session.query(Realisateurs).filter_by(realisateurs=scrap_realisateur).first() #le réalisateur existe dans cette liste
                if existing_real : #s'il existe dans la base
                    realisateur=existing_real #on le récupère juste (pour pouvoir l'associer ensuite) mais on le commit pas
                else : 
                    realisateur=Realisateurs(realisateur=scrap_realisateur) #on le récupère en l'instanciant
                    self.session.add(realisateur) #on l'ajoute pour le commit ensuite (ci dessous)
                    self.session.commit()
                #table realisateurslinkfilms (le faire pour chaque realisateur quand il y en a plusieurs par film)
                realisateurslinkfilms=RealisateursLinkFilms(id_film=film.id, id_realisateur=realisateur.id)
                self.session.add(realisateurslinkfilms)
                self.session.commit()
        else :
            scrap_realisateur=item['realisateur']
            existing_real = self.session.query(Realisateurs).filter_by(realisateurs=scrap_realisateur).first() #le réalisateur existe dans cette liste
            if existing_real : #s'il existe dans la base
                realisateur=existing_real #on le récupère juste (pour pouvoir l'associer ensuite) mais on le commit pas
            else: 
                realisateur=Realisateurs(realisateurs=scrap_realisateur) #on le récupère en l'instanciant
                self.session.add(realisateur) #on l'ajoute pour le commit ensuite (ci dessous)
                self.session.commit()
            #table realisateurslinkfilms (le faire pour chaque realisateur quand il y en a plusieurs par film)
            realisateurslinkfilms=RealisateursLinkFilms(id_film=film.id, id_realisateur=realisateur.id)
            self.session.add(realisateurslinkfilms)
            self.session.commit()
    
      #table acteurs
        if isinstance(item['acteurs'], list): # vérifier que l'élement est une liste
            for scrap_acteur in item['acteurs']: #pour chaque élément de la liste acteurs résultant du scrapping
                existing_act = self.session.query(Acteurs).filter_by(acteurs=scrap_acteur).first() #on teste si l'acteur existe en base
                if existing_act : #s'il existe
                    acteurs=existing_act #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
                else : #s'il n'existe pas
                    acteurs=Acteurs(acteurs=scrap_acteur) #on le stocke en base dans la table acteurs
                    self.session.add(acteurs) #ajouter l'acteur à la session
                    self.session.commit() #commiter la session
            #table acteurslinkfilms (le faire pour chaque acteur quand yen a plusieurs par film)
                acteurslinkfilms=ActeursLinkFilms(id_film=film.id, id_acteur=acteurs.id)
                self.session.add(acteurslinkfilms)
                self.session.commit()
        else:
            scrap_acteur=item['acteurs']
            existing_act = self.session.query(Acteurs).filter_by(acteurs=scrap_acteur).first() #on teste si l'acteur existe en base
            if existing_act : #s'il existe
                acteurs=existing_act #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
            else : 
                acteurs=Acteurs(acteurs=scrap_acteur)
                self.session.add(acteurs)
                self.session.commit()
            #table acteurslinkfilms (le faire pour chaque acteur quand yen a plusieurs par film)
            acteurslinkfilms=ActeursLinkFilms(id_film=film.id, id_acteur=acteurs.id)
            self.session.add(acteurslinkfilms)
            self.session.commit()

        #table pays
        if isinstance(item['pays'], list): #vérifier que mon élément est une liste
            for scrap_pays in item['pays']: #pour chaque élément de la liste pays
                existing_pays = self.session.query(Pays).filter_by(pays=scrap_pays).first() #on teste si le pays existe en base
                if existing_pays : #s'il existe
                    pays=existing_pays #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (table d'association)
                else : #s'il n'existe pas
                    pays=Pays(pays=scrap_pays) #on le stocke en base
                    self.session.add(pays) #ajouter le pays à la session
                    self.session.commit() #commiter la session
            #table payslinkfilms (le faire pour chaque pays quand il y en a plusieurs par film)
            payslinkfilms=PaysLinkFilms(id_film=film.id, id_pays=pays.id)
            self.session.add(payslinkfilms)
            self.session.commit()
        else:
            scrap_pays=item['pays']
            existing_pays = self.session.query(Pays).filter_by(pays=scrap_pays).first() #on teste si le pays existe en base
            if existing_pays : #s'il existe
                pays=existing_pays #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (table d'association)
            else : 
                pays=Pays(pays=scrap_pays)
                self.session.add(pays)
                self.session.commit()
            #table payslinkfilms (le faire pour chaque pays quand il y en a plusieurs par film)
            payslinkfilms=PaysLinkFilms(id_film=film.id, id_pays=pays.id)
            self.session.add(payslinkfilms)
            self.session.commit()

        #table genre
        if isinstance(item['genre'], list): #vérifier que mon élément est une liste
            for scrap_genre in item['genre']: #pour chaque élément de la liste genre
                existing_genre = self.session.query(Genre).filter_by(genre=scrap_genre).first() #on teste si le genre existe en base
                if existing_genre : #s'il existe
                    genre=existing_genre #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (pour la table d'association)
                else : #s'il n'existe pas
                    genre=Genre(genre=scrap_genre) #on le stocke en base dans sa table
                    self.session.add(genre) #ajouter le genre à la session
                    self.session.commit() #commiter la session
            #table genrelinkfilms (le faire pour chaque genre quand il y en a plusieurs par film)
            genrelinkfilms=GenreLinkFilms(id_film=film.id, id_genre=genre.id)
            self.session.add(genrelinkfilms)
            self.session.commit()
        else:
            existing_genre = self.session.query(Genre).filter_by(genre=scrap_genre).first() #on teste si le genre existe en base
            if existing_genre : #s'il existe
                genre=existing_genre #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (pour la table d'association)
            else :     
                genre=Genre(pays=item['genre'])
                self.session.add(genre)
                self.session.commit()
            #table genrelinkfilms (le faire pour chaque genre quand il y en a plusieurs par film)
            genrelinkfilms=GenreLinkFilms(id_film=film.id, id_genre=genre.id)
            self.session.add(genrelinkfilms)
            self.session.commit()
    
    def close_spider(self, spider):
        # Fermer la connexion à la base de données
        self.session.close() #

class BookscraperPipelineFilm:
        
        def process_item(self, item, spider): #méthode qui fait appel à une autre méthode
            item = self.cleaned_time(item)
            item = self.cleaned_date(item)
            item = self.cleaned_genre(item)
            item = self.cleaned_boxoffice(item)
            item = self.cleaned_pays(item)
            item = self.cleaned_acteurs(item)
            item = self.cleaned_scorespectateurs(item)
            item = self.cleaned_scorepresse(item)
            return item

        def cleaned_time(self, item): #version nettoyée de la durée instanciée en variable
            adapter = ItemAdapter(item)
            duree_raw = adapter.get('duree')
            if isinstance(duree_raw, list):
                duree_cleaned = ''.join(duree_raw)  #transforme la liste en phrase
                duree_cleaned = duree_cleaned.strip() #retire les caractères ou espaces encadrant le mot
            heure=0
            heure_match=re.search(r'(\d+)h', duree_cleaned) #recherche le nombre devant h
            minutes_match=re.search(r'(\d+)min', duree_cleaned) #recherche le nombre devant min
            if heure_match: #teste si l'heure existe
                heure=int(heure_match.group(1))*60 #transforme l'heure en minutes
                duree_new =heure+int(minutes_match.group(1)) #somme heure et minutes
                adapter['duree'] = duree_new
            else :
                adapter['duree'] = 0
            return item

        def cleaned_date(self, item): 
            adapter = ItemAdapter(item)
            annee_raw = adapter.get('annee')
            annee_cleaned = annee_raw.strip()
            #annee_cleaned = dateparser.parse(annee_cleaned, date_formats=['%d %B %Y'])
            adapter['annee'] = str(annee_cleaned)
            return item

        def cleaned_genre(self, item) :
            adapter = ItemAdapter(item)
            genre_raw = adapter.get('genre')
            genre_cleaned = ', '.join(genre_raw)   
            adapter['genre'] = genre_cleaned
            return item
            
        def cleaned_boxoffice(self, item) :
            adapter = ItemAdapter(item)
            boxoff = adapter.get('boxofficefr')
            if boxoff is not None:
                cleanbox = boxoff.strip().replace(" ","").replace("entrées","") # enleve l'espace et l'espace et entrées
                adapter['boxofficefr'] = int(cleanbox)
            else:
                adapter['boxofficefr'] = 0
            return item
        
        def cleaned_pays(self, item) :
            adapter = ItemAdapter(item)
            pays_cleaned = adapter.get('pays')
            if pays_cleaned is None:
                pays_cleaned = "N/C"
            else :
                pays_cleaned = pays_cleaned.strip()
            adapter['pays'] = str(pays_cleaned)
            return item
        
        def cleaned_acteurs(self, item) : 
            adapter = ItemAdapter(item)
            acteurs_raw = adapter.get('acteurs')
            if acteurs_raw is None:
                acteurs_cleaned = "N/C"
            else :
                if isinstance(acteurs_raw, list):
                    acteurs_cleaned =  ', '.join(acteurs_raw)  
                    acteurs_cleaned = acteurs_cleaned.strip()
                else : 
                    acteurs_cleaned = "N/C" 
            adapter['acteurs'] = str(acteurs_cleaned)
            return item
        
        def cleaned_scorespectateurs(self, item) : 
            adapter = ItemAdapter(item)
            scorespectateurs_raw = adapter.get('scorespectateurs')
            if scorespectateurs_raw is None:
                scorespectateurs_cleaned = None
            else :
                if isinstance(scorespectateurs_raw, float):
                    scorespectateurs_cleaned = scorespectateurs_raw.strip().replace(",",".")
                else : 
                   scorespectateurs_cleaned = None
            adapter['scorespectateurs'] = scorespectateurs_cleaned
            return item
        
        def cleaned_scorepresse(self, item) : 
            adapter = ItemAdapter(item)
            scorepresse_raw = adapter.get('scorepresse')
            if scorepresse_raw is None:
                scorepresse_cleaned = None
            else :
                if isinstance(scorepresse_raw, float):
                    scorepresse_cleaned = scorepresse_raw.strip().replace(",",".")
                else : 
                    scorepresse_cleaned = None
            adapter['scorepresse'] = scorepresse_cleaned
            return item        
        

    
###########################################################################################################################################################
###########################################################################################################################################################

# PIPELINE SERIES :

###########################################################################################################################################################
###########################################################################################################################################################


    def process_item(self, item, spider):
        # Insérer les données dans la base de données :
        # - règle pour vérifier l'existence de l'entité dans la table correspondante
        # - ajout de l'entité

        #table films
        # try : 
        existing_film = self.session.query(Films).filter_by(titre=item['titre'], annee=item['annee']).first()
        if existing_film is not None :
            film=existing_film
        else : 
            film=Films(titre=item['titre'], scorepresse = item['scorepresse'], scorespectateurs = item['scorespectateurs'], annee = item['annee'], duree = item['duree'], description = item['description'], boxofficefr = item['boxofficefr'])
            self.session.add(film)


class DatabasePipelineSeries :

    def open_spider(self, spider):
        # Se connecter à la base de données
        # Créer la table si elle n'existe pas
       
        ##### créer une connexion à la bdd postgre
        from bookscraper.orm import session
        self.session=session


    def process_item(self, item, spider):
        # Insérer les données dans la base de données
        existing_serie = self.session.query(Series).filter_by(titre=item['titre'], annee=item['annee']).first()
        if existing_serie is not None :
            series=existing_serie
        #table series
        else : 
            series=Series(titre=item['titre'], scorepresse = item['scorepresse'], scorespectateurs = item['scorespectateurs'], annee = item['annee'], duree = item['duree'], description = item['description'], saisons = item['saisons'], episodes = item['episodes'])
            self.session.add(series)
            self.session.commit()

       #table realisateurs
        if isinstance(item['realisateur'], list): # vérifier que l'élement est une liste
            for scrap_realisateur in item['realisateur']: #savoir si dans la liste de real scrappée
                existing_real = self.session.query(Realisateurs).filter_by(realisateurs=scrap_realisateur).first() #le réalisateur existe dans cette liste
                if existing_real : #s'il existe dans la base
                    realisateurs=existing_real #on le récupère juste (pour pouvoir l'associer ensuite) mais on le commit pas
                else : 
                    realisateurs=Realisateurs(realisateurs=scrap_realisateur) #on le récupère en l'instanciant
                    self.session.add(realisateur) #on l'ajoute pour le commit ensuite (ci dessous)
                    self.session.commit()
                #table realisateurslinkfilms (le faire pour chaque real quand yen a plusieurs par serie)
                realisateurslinkseries=RealisateursLinkSeries(id_series=series.id, id_realisateurs_realisateur.id)
                self.session.add(realisateurslinkseries)
                self.session.commit() 
        else:
            scrap_realisateur=item['realisateur']
            existing_real = self.session.query(Realisateurs).filter_by(realisateur=scrap_realisateur).first() #on teste si l'acteur existe en base
            if existing_real : #s'il existe
                realisateur=existing_real #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
            else : #s'il n'existe pas
                realisateur=Realisateurs(realisateur=scrap_realisateur) #on le récupère en l'instanciant
                self.session.add(realisateur) #on l'ajoute pour le commit ensuite (ci dessous)
                self.session.commit()
            #table realisateurslinkfilms (le faire pour chaque real quand yen a plusieurs par serie)
            realisateurslinkseries=RealisateursLinkSeries(id_serie=serie.id, id_realisateur=realisateur.id)
            self.session.add(realisateurslinkseries)
            self.session.commit()


        #table acteurs
        if isinstance(item['acteurs'], list): # vérifier que l'élement est une liste
            for scrap_acteur in item['acteurs']: #pour chaque élément de la liste acteurs résultant du scrapping
                existing_act = self.session.query(Acteurs).filter_by(acteur=scrap_acteur).first() #on teste si l'acteur existe en base
                if existing_act : #s'il existe
                    acteur=existing_act #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
                else : #s'il n'existe pas
                    acteur=Acteurs(acteur=scrap_acteur) #on le stocke en base dans la table acteurs
                    self.session.add(acteur) #ajouter l'acteur à la session
                    self.session.commit() #commiter la session
            #table acteurslinkfilms (le faire pour chaque acteur quand yen a plusieurs par serie)
                acteurslinkseries=ActeursLinkSeries(serie.id, acteur.id)
                self.session.add(acteurslinkseries)
                self.session.commit()
        else:
            scrap_acteur=item['acteurs']
            existing_act = self.session.query(Acteurs).filter_by(acteur=scrap_acteur).first() #on teste si l'acteur existe en base
            if existing_act : #s'il existe
                acteur=existing_act #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
            else : #s'il n'existe pas
                acteur=Acteurs(acteur=item['acteurs'])
                self.session.add(acteur)
                self.session.commit()
            #table acteurslinkfilms (le faire pour chaque acteur quand yen a plusieurs par serie)
            acteurslinkseries=ActeursLinkSeries(id_serie = series.id, id_acteur = acteurs.id)
            self.session.add(acteurslinkseries)
            self.session.commit()

        #table pays
        if isinstance(item['pays'], list): #vérifier que mon élément est une liste
            for scrap_pays in item['pays']: #pour chaque élément de la liste pays
                existing_pays = self.session.query(Pays).filter_by(pays=scrap_pays).first() #on teste si le pays existe en base
                if existing_pays : #s'il existe
                    pays=existing_pays #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (table d'association)
                else : #s'il n'existe pas
                    pays=Pays(pays=scrap_pays) #on le stocke en base
                    self.session.add(pays) #ajouter le pays à la session
                    self.session.commit() #commiter la session
                #table acteurslinkfilms (le faire pour chaque pays quand il y en a plusieurs par serie)
                payslinkseries=PaysLinkSeries(serie.id, pays.id)
                self.session.add(payslinkseries)
                self.session.commit()
        else:
            existing_pays = self.session.query(Pays).filter_by(pays=scrap_pays).first() #on teste si le pays existe en base
            if existing_pays : #s'il existe
                pays=existing_pays
            else:
                pays=Pays(pays=item['pays'])
                self.session.add(pays)
                self.session.commit()
            #table acteurslinkseries (le faire pour chaque pays quand il y en a plusieurs par serie)
            payslinkseries=PaysLinkSeries(serie.id, pays.id)
            self.session.add(payslinkseries)
            self.session.commit()

        #table genre
        if isinstance(item['genre'], list): #vérifier que mon élément est une liste
            for scrap_genre in item['genre']: #pour chaque élément de la liste genre
                existing_genre = self.session.query(Genre).filter_by(genre=scrap_genre).first() #on teste si le genre existe en base
                if existing_genre : #s'il existe
                    genre=existing_genre #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (pour la table d'association)
                else : #s'il n'existe pas
                    genre=Genre(genre=scrap_genre) #on le stocke en base dans sa table
                    self.session.add(genre) #ajouter le genre à la session
                    self.session.commit() #commiter la session
            #table genrelinkfilms (le faire pour chaque genre quand il y en a plusieurs par serie)
            genrelinkseries=GenreLinkSeries(serie.id, genre.id)
            self.session.add(genrelinkseries)
            self.session.commit()
        else:
            existing_genre = self.session.query(Genre).filter_by(genre=scrap_genre).first() #on teste si le genre existe en base
            if existing_genre : #s'il existe
                genre=existing_genre
            else :
                genre=Genre(genre=scrap_genre) #on le stocke en base dans sa table
                self.session.add(genre) #ajouter le genre à la session
                self.session.commit() #commiter la session
            #table genrelinkseries (le faire pour chaque genre quand il y en a plusieurs par serie)
            genrelinkseries=GenreLinkSeries(serie.id, genre.id)
            self.session.add(genrelinkseries)
            self.session.commit()

    
    def close_spider(self, spider):
        # Fermer la connexion à la base de données
        self.connection.commit()
        self.connection.close()

    
class BookscraperPipelineSeries:
        
        def process_item(self, item, spider): #méthode qui fait appel à une autre méthode
            item = self.cleaned_time(item)
            item = self.cleaned_date(item)
            item = self.cleaned_genre(item)
            item = self.cleaned_saisons(item)
            item = self.cleaned_episodes(item)
            item = self.cleaned_pays(item)
            item = self.cleaned_acteurs(item)
            item = self.cleaned_scorespectateurs(item)
            item = self.cleaned_scorepresse(item)
            return item

        def cleaned_time(self, item): #version nettoyée de la durée instanciée en variable
            adapter = ItemAdapter(item)
            duree_raw = adapter.get('duree')
            duree_cleaned = duree_raw.strip() #retire les sauts
            heure=0
            heure_match=re.search(r'(\d+) h', duree_cleaned) #recherche le nombre devant h
            minutes_match=re.search(r'(\d+) min', duree_cleaned) #recherche le nombre devant min
            if heure_match: #teste si l'heure existe
                heure = (int(heure_match.group(1)))*60 #transforme l'heure en minutes
                duree_new = heure+int(minutes_match.group(1)) #somme heure et minutes
                adapter['duree'] = duree_new
            else : 
                duree_new = int(minutes_match.group(1)) #transforme minutes en chiffre
                adapter['duree'] = duree_new
            return item

        def cleaned_date(self, item): 
            adapter = ItemAdapter(item)
            annee_raw = adapter.get('annee')
            match_date_lettres = re.search('\d{1,2}\s(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre)\s\d{4}', annee_raw)
            #match pour trouver une date en toutes lettres
            match_depuis = "Depuis" #match pour chercher depuis
            annee_cleaned = annee_raw.strip()#retire les caractères ou espaces encadrant le mot
            print(annee_raw)
            print(annee_cleaned)
            if match_date_lettres : 
                annee_cleaned = match_date_lettres.group()
                annee_cleaned = dateparser.parse(annee_cleaned, date_formats=['%d %B %Y'])
            else :
                if match_depuis in annee_raw : 
                    annee_cleaned = annee_cleaned.replace("Depuis", "").replace(" ","")#retire les caractères ou espaces encadrant le mot
                    annee_cleaned = annee_cleaned.replace("Sur AppleTV+", "").replace(" ","")#retire les caractères ou espaces encadrant le mot
                    annee_cleaned = annee_cleaned.replace("Sur Netflix", "").replace(" ","")#retire les caractères ou espaces encadrant le mot
                else :
                    annee_cleaned = annee_cleaned[0:5]
                    annee_cleaned = annee_cleaned.replace(" ","")
                    print(annee_cleaned)
            adapter['annee'] = annee_cleaned
            return item

        def cleaned_genre(self, item) :
            adapter = ItemAdapter(item)
            genre_raw = adapter.get('genre')
            genre_cleaned = ', '.join(genre_raw)   
            adapter['genre'] = genre_cleaned
            return item
            
        def cleaned_saisons(self, item) :
            adapter = ItemAdapter(item)
            sais = adapter.get('saisons')
            if sais is not None:
                cleansais = sais.strip().replace(" ","").replace("Saison","").replace("s","") # garde que les chiffres
                adapter['saisons'] = int(cleansais)
            else:
                adapter['saisons'] = 0
            return item
        
        def cleaned_episodes(self, item) :
            adapter = ItemAdapter(item)
            epis = adapter.get('episodes')
            if epis is not None:
                cleanepis = epis.strip().replace(" ","").replace("Episode","").replace("s","") # garde que les chiffres
                adapter['episodes'] = int(cleanepis)
            else:
                adapter['episodes'] = 0
            return item
        
        def cleaned_pays(self, item) :
            adapter = ItemAdapter(item)
            pays_cleaned = adapter.get('pays')
            if pays_cleaned is None:
                pays_cleaned = "N/C"
            else :
                pays_cleaned = pays_cleaned.strip()
            adapter['pays'] = str(pays_cleaned)
            return item
        
        def cleaned_acteurs(self, item) : 
            adapter = ItemAdapter(item)
            acteurs_raw = adapter.get('acteurs')
            if acteurs_raw is None:
                acteurs_cleaned = "N/C"
            else :
                if isinstance(acteurs_raw, list):
                    acteurs_cleaned =  ', '.join(acteurs_raw)  
                    acteurs_cleaned = acteurs_cleaned.strip()
                else : 
                    acteurs_cleaned = "N/C" 
            adapter['acteurs'] = str(acteurs_cleaned)
            return item
        
        def cleaned_scorespectateurs(self, item) : 
            adapter = ItemAdapter(item)
            scorespectateurs_raw = adapter.get('scorespectateurs')
            if scorespectateurs_raw is None:
                scorespectateurs_cleaned = None
            else :
                if isinstance(scorespectateurs_raw, float):
                    scorespectateurs_cleaned = scorespectateurs_raw.strip().replace(",",".")
                else : 
                    scorespectateurs_cleaned = None
            adapter['scorespectateurs'] = scorespectateurs_cleaned
            return item
        
        def cleaned_scorepresse(self, item) : 
            adapter = ItemAdapter(item)
            scorepresse_raw = adapter.get('scorepresse')
            if scorepresse_raw is None:
                scorepresse_cleaned = None
            else :
                if isinstance(scorepresse_raw, float):
                    scorepresse_cleaned = scorepresse_raw.strip().replace(",",".")
                else : 
                    scorepresse_cleaned = None
            adapter['scorepresse'] = scorepresse_cleaned
            return item  