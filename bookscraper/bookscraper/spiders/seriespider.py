import scrapy
    # coder une fonction pour parcourir les pages une par une avec yeld item a la fin
    # chemin d'un titre de film //li/div/div/h2/a

class SeriespiderSpider(scrapy.Spider):
    name = 'seriespider'
    allowed_domains = ['www.allocine.fr']
    start_urls = ["https://www.allocine.fr/series-tv/"]
    custom_settings = {"ITEM_PIPELINES" : {
    "bookscraper.pipelines.DatabasePipelineSeries": 200,
    "bookscraper.pipelines.BookscraperPipelineSeries": 100
}}
    i=1

    def __init__(self, category=None, *args, **kwargs): #initialisation de la méthode / surcharge de la méthode BookspiderSpider
        super(SeriespiderSpider, self).__init__(*args, **kwargs)
        self.i = 0

    def parse(self, response):
        series_url = response.xpath("//a[@class='meta-title-link']/@href") #liste avec les raccourci permettant de reconnaitre chaque lien vers un film
        for serie_url in series_url : # itération se répétant pour chaque lien présent dans la liste books
            yield response.follow(serie_url, self.parse_item)
        
        self.i=self.i+1
        next_page = (f"?page={self.i}") #chemin permettant de reconnaitre chaque lien vers la page suivante
        yield response.follow(next_page, callback=self.parse)

        ########## print pour montrer les logs
        print("--------------------------------------------")
        print("--------------------------------------------\n")
        print(self.i)
        print(next_page)


    def parse_item(self, response):
        yield {
            'titre' : response.xpath(".//div[@class='titlebar-title titlebar-title-xl']/span/text()").get(),
            'scorepresse' : response.xpath("(//div[@class='stareval stareval-small stareval-theme-default']//span[@class='stareval-note'])[1]/text()").get(),
            'scorespectateurs' : response.xpath("(//div[@class='stareval stareval-small stareval-theme-default']//span[@class='stareval-note'])[2]/text()").get(),
            'genre' : response.xpath(".//span[@class='spacer'][2]/following-sibling::*/text()").getall(),
            'annee' : response.xpath("//div[@class='meta-body-item meta-body-info']/text()[1]").get(),
            'duree' : response.xpath(".//div[@class='meta-body-item meta-body-info']/text()[2]").get(),
            'description' : response.xpath(".//div[@class='content-txt ']/p/text()").get(),
            'acteurs' : response.xpath(".//div[@class='meta-body-item meta-body-actor']/span[position()>1]/text()").getall(),
            'realisateur' : response.xpath(".//span[text()='Créée par']/following-sibling::*/text()").get(),
            'saisons' : response.xpath(".//div[@class='stats-numbers-row stats-numbers-seriespage']/div/div/text()").get(), 
            'episodes' : response.xpath(".//div[@class='stats-numbers-row stats-numbers-seriespage']/div[2]/div/text()").get(),
            'pays' : response.xpath(".//span[text()='Nationalité']/following-sibling::*/text()").get()
            }