# -*- coding: utf-8 -*-

import scrapy
from scrapy.http import Request, FormRequest
from tools.basic_tool import Utils
from items import UsmItem


__author__ = "Carl Theodoro Posthuma Solis && Josué Fabricio Urbina González"


class ResearchGate(scrapy.Spider):
    name = "research_gate"
    login_url = "https://www.researchgate.net/login"
    start_urls = [login_url]
    browser = 5
    STATUS_OK = 200

    custom_settings = {'DOWNLOAD_DELAY': '3',
                       'CONCURRENT_REQUESTS': '1',
                       'COOKIES_ENABLED': 'True'}

    def __init__(self, source=None, *args, **kwargs):
        super(ResearchGate, self).__init__(*args, **kwargs)
        if source is not None:
            self.source = source
        else:
            self.source = ""
        self.filter = None

    def parse(self, response):
        return Request(url=self.login_url, callback=self.login)

    def login(self, response):
        token = response.css('input[name="request_token"]::attr(value)').extract_first()

        data = {'login': 'ivanvladimir@turing.iimas.unam.mx',
                'password': '',
                'request_token': token,
                'invalidPasswordCount': '0',
                'setLoginCookie': 'yes'}

        return FormRequest.from_response(response,
                                         formdata=data,
                                         callback=self.valid_login)

    def valid_login(self, response):

        # TODO make this list from people
        search = Utils.get_query_param(self.source)

        url_tail = search[2].strip().replace(' ', '%20')

        # search_list = ["https://www.researchgate.net/search.Search.html?type=researcher&query=HUGO%20MAURICIO%20CASTREJON%20MENDOZA"]

        if "Ivan Meza" in str(response.body):
            self.log("Successfully logged in")
            yield Request(url="https://www.researchgate.net/search.Search.html?type=researcher&query=" + url_tail,
                          callback=self.parse_myrg, meta={'id_person': search[0],
                                                          'attr': search[1],
                                                          'search': search[2],
                                                          'num_snip': 0})

        else:
            self.log("Wrong credentials")

    def parse_myrg(self, response):

        black_list = ['1', ' ', '[...]', 'Recommendation', 'Download', 'Recommend', 'Follow', 'Share',
                      'Request full-text']
        black_list2 = ['Referenced in the project:', 'Research from: ', ' ']

        itemproc = self.crawler.engine.scraper.itemproc

        id_person = response.meta['id_person']
        base_attr = response.meta['attr']
        search = response.meta['search']
        num_snippet = response.meta['num_snip']

        for search_box in response.xpath('//div[contains(@class, "search-box__result-item")]'):

            storage_item = UsmItem()

            num_snippet = num_snippet + 1

            text = ' '.join(list(set(search_box.css('span::text').extract()) - set(black_list)) + list(
                set(search_box.css('div::text').extract()) - set(black_list2)))
            url = response.url
            title_list = search_box.css('a.nova-e-link--theme-bare ::text').extract()

            try:
                if title_list[0] == 'Source':
                    title = title_list[1]
                else:
                    title = title_list[0]
            except:
                title = "NO TITLE WAS FOUND, YOUR SCRAPER SUCKS!"
            # print(url, title, text, "\n\n\n\n")

            storage_item['title'] = title
            storage_item['cite'] = url
            storage_item['text'] = text
            storage_item['engine_search'] = self.browser

            storage_item['id_person'] = id_person
            storage_item['search'] = search
            storage_item['attr'] = base_attr
            storage_item['number_snippet'] = num_snippet

            itemproc.process_item(storage_item, self)

# nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare
# nova-e-link nova-e-link--color-inherit nova-e-link--theme-bare


# "0": {
#     "number_snippet": "1",
#     "title": "20+ Andres Cruz Gonzalez profiles | LinkedIn",
#     "search": "CRUZ GONZALEZ ANDRES DE LA ",
#     "cite": "https://www.linkedin.com/pub/dir/ANDRES/CRUZ+GONZALEZ/",
#     "text": "03/09/2018\u00a0\u00b7 View the profiles of professionals named Andres Cruz Gonzalez on LinkedIn. There are 20+ professionals named Andres Cruz Gonzalez\u2026",
#     "id_person": "726",
#     "engine_search": "4"
# }
#
# "0": {
#     "number_snippet": "1",
#     "title": "Co-manejo pesquero en la Reserva Marina de Galápagos",
#     "search": "CRUZ GONZALEZ ANDRES DE LA ",
#     "cite": "https://www.researchgate.net/search.Search.html?type=researcher&query=HUGO%20MAURICIO%20CASTREJON%20MENDOZA",
#     "text": "Jan 2011" + "Fundación Charles Darwin-Kanankil/Plaza y Valdez" + "Mauricio Castrejon" + """
#     Las Islas Galápagos representan un icono a nivel mundial por su biodiversidad y el alto nivel de endemismo que las caracteriza. Sus ricos y diversos ecosistemas marinos han sido históricamente objeto de la actividad pesquera, especialmente a partir de la década de los 90s, periodo en el que se registró un importante desarrollo de la flota pesquera artesanal. Este hecho condujo en marzo de 1998 a la implementación de un esquema de co-manejo, cuyo objetivo principal fue controlar el acceso y nivel de explotación de los recursos marinos (particularmente de los recursos pesqueros) de la recién creada Reserva Marina de Galápagos (RMG). Lamentablemente, la institucionalización y aplicación de este tipo de esquema de manejo per se aún no ha logrado garantizar con éxito la sostenibilidad de las pesquerías y el bienestar socio-económico del sector pesquero artesanal de Galápagos. El presente documento, desarrollado por Mauricio Castrejón Mendoza, representa una contribución clave para profundizar en el esquema de co-manejo de las pesquerías de Galápagos. Con claridad y rigurosidad, el autor relata la historia y tendencias de explotación de los principales recursos pesqueros en Galápagos, así como los éxitos y fracasos asociados al marco legal e institucional de manejo. Asimismo, identifica, señala y discute aspectos ecológico-pesqueros, socio-económicos y legales críticos para revertir los problemas detectados en el sistema de co-manejo de las pesquerías artesanales de Galápagos. Además, sustenta sus aseveraciones en resultados generados con herramientas cuantitativas de actualidad, arribando a varias recomendaciones específicas, concretas y útiles, tanto para los científicos como para los tomadores de decisiones. El análisis minucioso, comprehensivo y crítico de dichas pesquerías le confiere una innegable importancia para el mejoramiento del sistema de co-manejo pesquero de la RMG.
#     """,
#     "id_person": "726",
#     "engine_search": "5"
# }
#
