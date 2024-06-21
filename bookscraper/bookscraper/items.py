# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

# chemin des films https://www.allocine.fr/films/genre-13027/

class BookscraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # coder une fonction pour parcourir les pages une par une avec yeld item a la fin
    # chemin d'un titre de film //li/div/div/h2/a
    titre = scrapy.Field()
    scorepresse = scrapy.Field()
    scorespectateurs = scrapy.Field()
    genre = scrapy.Field()
    annee = scrapy.Field()
    duree = scrapy.Field()
    description = scrapy.Field()
    acteurs = scrapy.Field()
    realisateur = scrapy.Field()
    pays = scrapy.Field()
    boxofficefr = scrapy.Field()

class SeriescraperItem(scrapy.Item):

    titre = scrapy.Field()
    scorepresse = scrapy.Field()
    scorespectateurs = scrapy.Field()
    genre = scrapy.Field()
    annee = scrapy.Field()
    duree = scrapy.Field()
    description = scrapy.Field()
    acteurs = scrapy.Field()
    realisateur = scrapy.Field()
    saisons = scrapy.Field()
    episodes = scrapy.Field()
    pays = scrapy.Field()
