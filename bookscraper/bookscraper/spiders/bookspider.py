import scrapy
    # coder une fonction pour parcourir les pages une par une avec yeld item a la fin
    # chemin d'un titre de film //li/div/div/h2/a

class BookspiderSpider(scrapy.Spider):
    name = 'bookspider'
    allowed_domains = ['www.allocine.fr']
    start_urls = ["https://www.allocine.fr/films/genre-13027/"]
    custom_settings = {"ITEM_PIPELINES" : {
    "bookscraper.pipelines.DatabasePipelineFilm": 200,
    "bookscraper.pipelines.BookscraperPipelineFilm": 100
}}
    i=1

    def __init__(self, category=None, *args, **kwargs): #initialisation de la méthode / surcharge de la méthode BookspiderSpider
        super(BookspiderSpider, self).__init__(*args, **kwargs)
        self.i = 0

    def parse(self, response):
        films = response.xpath('//li/div/div/h2') #liste avec les raccourci permettant de reconnaitre chaque lien vers un film
        for film in films : # itération se répétant pour chaque lien présent dans la liste books
            film_url = film.xpath('./a').attrib['href']
            yield response.follow(film_url, self.parse_item)
        
        self.i=self.i+1
        next_page = (f"?page={self.i}") #chemin permettant de reconnaitre chaque lien vers la page suivante
        yield response.follow(next_page, callback=self.parse)

        ########## print pour montrer les logs
        print("--------------------------------------------")
        print("--------------------------------------------\n")
        print(self.i)
        print(next_page)


    def parse_item(self, response):
        #begin_path = "//div[@class='card entity-card entity-card-list cf entity-card-player-ovw']"
        yield {
            'titre' : response.xpath(".//div[@class='titlebar-title titlebar-title-xl']/text()").get(),
            'scorepresse' : response.xpath("(//div[@class='stareval stareval-small stareval-theme-default']//span[@class='stareval-note'])[1]/text()").get(),
            'scorespectateurs' : response.xpath("(//div[@class='stareval stareval-small stareval-theme-default']//span[@class='stareval-note'])[2]/text()").get(),
            'genre' : response.xpath(".//span[@class='spacer'][2]/following-sibling::*/text()").getall(),
            'annee' : response.xpath(".//div[@class='meta-body-item meta-body-info']/span[1]/text()").get(),
            'duree' : response.xpath(".//div[@class='meta-body-item meta-body-info']/text()").getall(),
            'description' : response.xpath(".//div[@class='content-txt ']/p/text()").get(),
            'acteurs' : response.xpath(".//div[@class='meta-body-item meta-body-actor']/span[position()>1]/text()").getall(),
            'realisateur' : response.xpath(".//div[@class='meta-body-item meta-body-direction meta-body-oneline'][1]/span[2]/text()").get(),
            'boxofficefr' : response.xpath(".//span[text()='Box Office France']/following-sibling::*/text()").get(),
            'pays' : response.xpath(".//span[text()='Nationalité']/following-sibling::*/span/text()").get()
            }