
#####################################################################################################
###############################                                       ###############################
###############################         ALLOCINE.com SCRAPPER         ###############################
###############################            movies & series            ###############################
###############################                  v2                   ###############################
#####################################################################################################

################ Before get started ##############

####### database, flexible server, RG and factory creation on Azure ######
> create a DDBB on Azure thanks to the script RG azure
> get on the "script_RG_azure" repository with cmd:
cd script_RG_azure
> then execute the script
./creation_RG.sh
> create a DB online in your flexible server (named scrapy_imdb)

####### install virtual environment on you computer ######
> I recommend you to install poetry environnement on your computer
> Then get on the first "bookscrapper" repository with cmd:
cd bookscraper

######### FILMS #########
launch spider with cmd  :
scrapy crawl bookspider

This will populate a films table on azure

######### SERIES #########
launch spider with cmd  :
scrapy crawl seriespider

This will populate a series table on azure

###############################################################























#####################################################################################################
###############################                                       ###############################
###############################         ALLOCINE.com SCRAPPER         ###############################
###############################            movies & series            ###############################
###############################                  v1                   ###############################
#####################################################################################################

######### Before get started ########
I recommend you to install poetry environnement on your computer
Then get on the first "bookscrapper" repository with cmd:
cd bookscraper

######### FILMS #########
launch spider with cmd  :
scrapy crawl bookspider

This will generate a films.db file on your repository

######### SERIES #########
launch spider with cmd  :
scrapy crawl seriespider

This will generate a series.db file on your repository

######### TEASING FUTURE FIX #########
In this release, there are only 2 database files generated thanks to sqlite3.
The next realease will consist of SQLAlchemy code instead of sqlite3.

For more details please go to the Database_Schemafor_future_fix repository

This fix will permit you to get the followings : 

######### one database
films_and_series.db as fs

######### several tables
fs.films
fs.series

fs.acteurs
fs.acteur_match_film
fs.acteur_match_series

fs.realisateurs
fs.realisateurs_match_film
fs.realisateurs_match_series

fs.genre
fs.genre_match_film
fs.genre_match_series
