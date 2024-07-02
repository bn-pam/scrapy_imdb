# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlalchemy, psycopg2
import re, dateparser, datetime
from models import Films, Series, Realisateurs, RealisateursLinkFilms, RealisateursLinkSeries, Acteurs, ActeursLinkFilms
from models import ActeursLinkSeries, Genre, GenreLinkFilms, GenreLinkSeries, Pays, PaysLinkFilms, PaysLinkSeries

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
        self.connection = psycopg2.connect(
            host="localhost", #à adapter
            database="film_scraping", #à adapter
            user="pbo", #à adapter
            password="123456") #à adapter

        self.curr = self.connection.cursor()


    def process_item(self, item, spider):
        # Insérer les données dans la base de données :
        # - règle pour vérifier l'existence de l'entité dans la table correspondante
        # - ajout de l'entité

        #table films
        existing_film = self.curr.query(Films).filter_by(titre=item['titre'], annee=item['annee']).first()
        if existing_film :
            pass
        else : 
            film=Films(titre=item['titre'], scorepresse = item['scorepresse'], scorespectateurs = item['scorespectateurs'], annee = item['annee'], duree = item['duree'], description = item['description'], boxeofficefr = item['boxofficefr'])
            self.curr.add(film)
            self.curr.commit()
        
        #table realisateurs
        if isintance(item['realisateurs'], list): # vérifier que l'élement est une liste
            for scrap_realisateur in item['realisateurs']: #savoir si dans la liste de real scrappée
                existing_real = self.curr.query(Realisateurs).filter_by(realisateur=scrap_realisateur).first() #le réalisateur existe dans cette liste
                if existing_real : #s'il existe dans la base
                    realisateur=existing_real #on le récupère juste (pour pouvoir l'associer ensuite) mais on le commit pas
                else : 
                    realisateur=Realisateurs(realisateur=scrap_realisateur) #on le récupère en l'instanciant
                    self.curr.add(realisateur) #on l'ajoute pour le commit ensuite (ci dessous)
                    self.curr.commit()
                #table realisateurslinkfilms (le faire pour chaque realisateur quand il y en a plusieurs par film)
                realisateurslinkfilms=RealisateursLinkFilms(film.id, realisateur.id)
                self.curr.add(realisateurslinkfilms)
                self.curr.commit()
        else :
            existing_real = self.curr.query(Realisateurs).filter_by(realisateur=scrap_realisateur).first() #le réalisateur existe dans cette liste
            if existing_real : #s'il existe dans la base
                realisateur=existing_real #on le récupère juste (pour pouvoir l'associer ensuite) mais on le commit pas
            else: 
                realisateur=Realisateurs(realisateur=scrap_realisateur) #on le récupère en l'instanciant
                self.curr.add(realisateur) #on l'ajoute pour le commit ensuite (ci dessous)
                self.curr.commit()
            #table realisateurslinkfilms (le faire pour chaque realisateur quand il y en a plusieurs par film)
            realisateurslinkfilms=RealisateursLinkFilms(film.id, realisateur.id)
            self.curr.add(realisateurslinkfilms)
            self.curr.commit()
    
      #table acteurs
        if isintance(item['acteurs'], list): # vérifier que l'élement est une liste
            for scrap_acteur in item['acteurs']: #pour chaque élément de la liste acteurs résultant du scrapping
                existing_act = self.curr.query(Acteurs).filter_by(acteur=scrap_acteur).first() #on teste si l'acteur existe en base
                if existing_act : #s'il existe
                    acteur=existing_act #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
                else : #s'il n'existe pas
                    acteur=Acteurs(acteur=scrap_acteur) #on le stocke en base dans la table acteurs
                    self.curr.add(acteur) #ajouter l'acteur à la session
                    self.curr.commit() #commiter la session
            #table acteurslinkfilms (le faire pour chaque acteur quand yen a plusieurs par film)
                acteurslinkfilms=ActeursLinkFilms(film.id, acteur.id)
                self.curr.add(acteurslinkfilms)
                self.curr.commit()
        else:
            existing_act = self.curr.query(Acteurs).filter_by(acteur=scrap_acteur).first() #on teste si l'acteur existe en base
            if existing_act : #s'il existe
                acteur=existing_act #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
            else : 
                acteur=Acteur(acteur=item['acteurs'])
                self.curr.add(acteur)
                self.curr.commit()
            #table acteurslinkfilms (le faire pour chaque acteur quand yen a plusieurs par film)
            acteurslinkfilms=ActeursLinkFilms(film.id, acteur.id)
            self.curr.add(acteurslinkfilms)
            self.curr.commit()

        #table pays
        if isintance(item['pays'], list): #vérifier que mon élément est une liste
            for scrap_pays in item['pays']: #pour chaque élément de la liste pays
                existing_pays = self.curr.query(Pays).filter_by(pays=scrap_pays).first() #on teste si le pays existe en base
                if existing_pays : #s'il existe
                    pays=existing_pays #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (table d'association)
                else : #s'il n'existe pas
                    pays=Pays(pays=scrap_pays) #on le stocke en base
                    self.curr.add(pays) #ajouter le pays à la session
                    self.curr.commit() #commiter la session
            #table payslinkfilms (le faire pour chaque pays quand il y en a plusieurs par film)
            payslinkfilms=PaysLinkFilms(film.id, pays.id)
            self.curr.add(payslinkfilms)
            self.curr.commit()
        else:
            existing_pays = self.curr.query(Pays).filter_by(pays=scrap_pays).first() #on teste si le pays existe en base
            if existing_pays : #s'il existe
                pays=existing_pays #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (table d'association)
            else : 
                pays=Pays(pays=item['pays'])
                self.curr.add(pays)
                self.curr.commit()
            #table payslinkfilms (le faire pour chaque pays quand il y en a plusieurs par film)
            payslinkfilms=PaysLinkFilms(film.id, pays.id)
            self.curr.add(payslinkfilms)
            self.curr.commit()

        #table genre
        if isintance(item['genre'], list): #vérifier que mon élément est une liste
            for scrap_genre in item['genre']: #pour chaque élément de la liste genre
                existing_genre = self.curr.query(Genre).filter_by(genre=scrap_genre).first() #on teste si le genre existe en base
                if existing_genre : #s'il existe
                    genre=existing_genre #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (pour la table d'association)
                else : #s'il n'existe pas
                    genre=Genre(genre=scrap_genre) #on le stocke en base dans sa table
                    self.curr.add(genre) #ajouter le genre à la session
                    self.curr.commit() #commiter la session
            #table genrelinkfilms (le faire pour chaque genre quand il y en a plusieurs par film)
            genrelinkfilms=GenreLinkFilms(film.id, genre.id)
            self.curr.add(genrelinkfilms)
            self.curr.commit()
        else:
            existing_genre = self.curr.query(Genre).filter_by(genre=scrap_genre).first() #on teste si le genre existe en base
            if existing_genre : #s'il existe
                genre=existing_genre #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (pour la table d'association)
            else :     
                genre=Genre(pays=item['genre'])
                self.curr.add(genre)
                self.curr.commit()
            #table genrelinkfilms (le faire pour chaque genre quand il y en a plusieurs par film)
            genrelinkfilms=GenreLinkFilms(film.id, genre.id)
            self.curr.add(genrelinkfilms)
            self.curr.commit()
    
    def close_spider(self, spider):
        # Fermer la connexion à la base de données
        self.connection.commit()
        self.connection.close()

class BookscraperPipelineFilm:
        
        def process_item(self, item, spider): #méthode qui fait appel à une autre méthode
            item = self.cleaned_time(item)
            item = self.cleaned_date(item)
            item = self.cleaned_genre(item)
            item = self.cleaned_boxoffice(item)
            item = self.cleaned_pays(item)
            item = self.cleaned_acteurs(item)
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
            duree_raw = adapter.get('annee')
            duree_cleaned = duree_raw.strip()
            duree_cleaned = dateparser.parse(duree_cleaned, date_formats=['%d %B %Y'])
            adapter['annee'] = duree_cleaned
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
        

    
###########################################################################################################################################################
###########################################################################################################################################################

# PIPELINE SERIES :

###########################################################################################################################################################
###########################################################################################################################################################


class DatabasePipelineSeries :

    def open_spider(self, spider):
        # Se connecter à la base de données
        # Créer la table si elle n'existe pas
       
       ##### créer une connexion à la bdd postgre
        self.connection = psycopg2.connect(
            host="localhost", #à adapter
            database="film_scraping", #à adapter
            user="pbo", #à adapter
            password="123456") #à adapter

        self.curr = self.connection.cursor()


    def process_item(self, item, spider):
        # Insérer les données dans la base de données

        #table series
        serie=Series(titre=item['titre'], scorepresse = item['scorepresse'], scorespectateurs = item['scorespectateurs'], annee = item['annee'], duree = item['duree'], description = item['description'], saisons = item['saisons'], episodes = item['episodes'])
        self.curr.add(serie)
        self.curr.commit()

       #table realisateurs
        if isintance(item['realisateurs'], list): # vérifier que l'élement est une liste
            for scrap_realisateur in item['realisateurs']: #savoir si dans la liste de real scrappée
                existing_real = self.curr.query(Realisateurs).filter_by(realisateur=scrap_realisateur).first() #le réalisateur existe dans cette liste
                if existing_real : #s'il existe dans la base
                    realisateur=existing_real #on le récupère juste (pour pouvoir l'associer ensuite) mais on le commit pas
                else : 
                    realisateur=Realisateurs(realisateur=scrap_realisateur) #on le récupère en l'instanciant
                    self.curr.add(realisateur) #on l'ajoute pour le commit ensuite (ci dessous)
                    self.curr.commit()
                #table realisateurslinkfilms (le faire pour chaque real quand yen a plusieurs par serie)
                realisateurslinkseries=RealisateursLinkSeries(series.id, realisateur.id)
                self.curr.add(realisateurslinkseries)
                self.curr.commit() 
        else:
            existing_real = self.curr.query(Realisateurs).filter_by(realisateur=scrap_realisateur).first() #on teste si l'acteur existe en base
            if existing_real : #s'il existe
                realisateur=existing_real #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
            else : #s'il n'existe pas
                realisateur=Realisateurs(realisateur=scrap_realisateur) #on le récupère en l'instanciant
                self.curr.add(realisateur) #on l'ajoute pour le commit ensuite (ci dessous)
                self.curr.commit()
            #table realisateurslinkfilms (le faire pour chaque real quand yen a plusieurs par serie)
            realisateurslinkseries=RealisateursLinkSeries(series.id, realisateur.id)
            self.curr.add(realisateurslinkseries)
            self.curr.commit()


        #table acteurs
        if isintance(item['acteurs'], list): # vérifier que l'élement est une liste
            for scrap_acteur in item['acteurs']: #pour chaque élément de la liste acteurs résultant du scrapping
                existing_act = self.curr.query(Acteurs).filter_by(acteur=scrap_acteur).first() #on teste si l'acteur existe en base
                if existing_act : #s'il existe
                    acteur=existing_act #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
                else : #s'il n'existe pas
                    acteur=Acteurs(acteur=scrap_acteur) #on le stocke en base dans la table acteurs
                    self.curr.add(acteur) #ajouter l'acteur à la session
                    self.curr.commit() #commiter la session
            #table acteurslinkfilms (le faire pour chaque acteur quand yen a plusieurs par serie)
                acteurslinkseries=ActeursLinkSeries(serie.id, acteur.id)
                self.curr.add(acteurslinkseries)
                self.curr.commit()
        else:
            existing_act = self.curr.query(Acteurs).filter_by(acteur=scrap_acteur).first() #on teste si l'acteur existe en base
            if existing_act : #s'il existe
                acteur=existing_act #on le stocke dans une variable pour pouvoir le réutiliser dans notre code
            else : #s'il n'existe pas
                acteur=Acteur(acteur=item['acteurs'])
                self.curr.add(acteur)
                self.curr.commit()
            #table acteurslinkfilms (le faire pour chaque acteur quand yen a plusieurs par serie)
            acteurslinkseries=ActeursLinkSeries(serie.id, acteur.id)
            self.curr.add(acteurslinkseries)
            self.curr.commit()

        #table pays
        if isintance(item['pays'], list): #vérifier que mon élément est une liste
            for scrap_pays in item['pays']: #pour chaque élément de la liste pays
                existing_pays = self.curr.query(Pays).filter_by(pays=scrap_pays).first() #on teste si le pays existe en base
                if existing_pays : #s'il existe
                    pays=existing_pays #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (table d'association)
                else : #s'il n'existe pas
                    pays=Pays(pays=scrap_pays) #on le stocke en base
                    self.curr.add(pays) #ajouter le pays à la session
                    self.curr.commit() #commiter la session
                #table acteurslinkfilms (le faire pour chaque pays quand il y en a plusieurs par serie)
                payslinkseries=PaysLinkSeries(serie.id, pays.id)
                self.curr.add(payslinkseries)
                self.curr.commit()
        else:
            existing_pays = self.curr.query(Pays).filter_by(pays=scrap_pays).first() #on teste si le pays existe en base
            if existing_pays : #s'il existe
                pays=existing_pays
            else:
                pays=Pays(pays=item['pays'])
                self.curr.add(pays)
                self.curr.commit()
            #table acteurslinkseries (le faire pour chaque pays quand il y en a plusieurs par serie)
            payslinkseries=PaysLinkSeries(serie.id, pays.id)
            self.curr.add(payslinkseries)
            self.curr.commit()

        #table genre
        if isintance(item['genre'], list): #vérifier que mon élément est une liste
            for scrap_genre in item['genre']: #pour chaque élément de la liste genre
                existing_genre = self.curr.query(Genre).filter_by(genre=scrap_genre).first() #on teste si le genre existe en base
                if existing_genre : #s'il existe
                    genre=existing_genre #on le stocke dans une variable pour pouvoir le réutiliser dans notre code (pour la table d'association)
                else : #s'il n'existe pas
                    genre=Genre(genre=scrap_genre) #on le stocke en base dans sa table
                    self.curr.add(genre) #ajouter le genre à la session
                    self.curr.commit() #commiter la session
            #table genrelinkfilms (le faire pour chaque genre quand il y en a plusieurs par serie)
            genrelinkseries=GenreLinkSeries(serie.id, genre.id)
            self.curr.add(genrelinkseries)
            self.curr.commit()
        else:
            existing_genre = self.curr.query(Genre).filter_by(genre=scrap_genre).first() #on teste si le genre existe en base
            if existing_genre : #s'il existe
                genre=existing_genre
            else :
                genre=Genre(genre=scrap_genre) #on le stocke en base dans sa table
                self.curr.add(genre) #ajouter le genre à la session
                self.curr.commit() #commiter la session
            #table genrelinkseries (le faire pour chaque genre quand il y en a plusieurs par serie)
            genrelinkseries=GenreLinkSeries(serie.id, genre.id)
            self.curr.add(genrelinkseries)
            self.curr.commit()

    
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