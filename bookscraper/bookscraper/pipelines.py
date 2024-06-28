# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlalchemy, psycopg2
import re, dateparser, datetime
from models import Films

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
            user="root", #à adapter
            password="123456") #à adapter

        self.curr = self.connection.cursor()


    def process_item(self, item, spider):
        # Insérer les données dans la base de données
        film=Films(titre=item['titre'], )

        # self.cursor.execute('''
        #     INSERT INTO films(
        #         titre,
        #         scorepresse,
        #         scorespectateurs,
        #         genre,
        #         annee,
        #         duree,
        #         description,
        #         acteurs,
        #         realisateur,
        #         pays,
        #         boxofficefr)
        #         VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        # ''', 
        # (item['titre'],
        # item['scorepresse'],
        # item['scorespectateurs'],
        # item['genre'],
        # item['annee'],
        # item['duree'],
        # item['description'],
        # item['acteurs'],
        # item['realisateur'],
        # item['pays'],
        # item['boxofficefr']))
        # self.connection.commit()
        # return item
    
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
        self.connection = sqlite3.connect('series.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS series(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT,
                scorepresse REAL,
                scorespectateurs REAL,
                genre TEXT,
                annee TEXT,
                duree INTEGER,
                description TEXT,
                acteurs TEXT,
                realisateur TEXT,
                saisons INTEGER,
                episodes INTEGER,
                pays TEXT
            )
        ''')
        self.connection.commit()


    def close_spider(self, spider):
        # Fermer la connexion à la base de données
        self.connection.commit()
        self.connection.close()

    def process_item(self, item, spider):
        # Insérer les données dans la base de données
        self.cursor.execute('''
            INSERT INTO series(
                titre,
                scorepresse,
                scorespectateurs,
                genre,
                annee,
                duree,
                description,
                acteurs,
                realisateur,
                saisons,
                episodes,
                pays)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', 
        (item['titre'],
        item['scorepresse'],
        item['scorespectateurs'],
        item['genre'],
        item['annee'],
        item['duree'],
        item['description'],
        item['acteurs'],
        item['realisateur'],
        item['saisons'],
        item['episodes'],
        item['pays']))
        self.connection.commit()
        return item
    
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