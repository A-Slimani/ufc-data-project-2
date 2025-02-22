from scrapy.selector.unified import Selector
from UFCScraper.pipelines import FightPipeline
from UFCScraper.items import FightItem
import psycopg2
import scrapy
import os

class UFCFightsSpider(scrapy.Spider):
    name = "initial_fights"
    allowed_domains = ["www.ufc.com"]
    start_urls = ["https://www.ufc.com/"]

    def clean_text(self, text) -> str:
        if text is None:
            return ""
        else:
            return text.replace("\n", "").strip()

    def parse(self, response):
        conn = psycopg2.connect(os.getenv("DB_URI"))
        cursor = conn.cursor()
        cursor.execute("SELECT url FROM events;")
        event_list = cursor.fetchall()
        # for event in event_list:
        #     yield response.follow(url=event[0], callback=self.parse_fights)
        for x in range(30):
            yield response.follow(url=event_list[x][0], callback=self.parse_fights)

    def parse_fights(self, response):
        selector = Selector(text=response.text)

        fights = selector.xpath("//div[@class='c-listing-fight__content']")
        for fight in fights:
            r_fighter = fight.xpath(".//div[@class='c-listing-fight__corner-name c-listing-fight__corner-name--red']/a/@href").get()
            b_fighter = fight.xpath(".//div[@class='c-listing-fight__corner-name c-listing-fight__corner-name--blue']/a/@href").get()

            round = fight.xpath(".//div[@class='c-listing-fight__result-text round']/text()").get()
            method = fight.xpath(".//div[@class='c-listing-fight__result-text method']/text()").get()
            time = fight.xpath(".//div[@class='c-listing-fight__result-text time']/text()").get()
            bout_weight = fight.xpath(".//div[@class='c-listing-fight__class-text']/text()").get()
            r_fighter_status = ''
            b_fighter_status = ''
            
            r_fighter_corner = fight.xpath(".//div[@class='c-listing-fight__corner-body--red']")
            b_fighter_corner = fight.xpath(".//div[@class='c-listing-fight__corner-body--blue']")
            
            if self.clean_text(r_fighter_corner.xpath(".//div[@class='c-listing-fight__outcome--win']/text()").get()):
                r_fighter_status = 'win'
                b_fighter_status = 'loss'
            elif self.clean_text(b_fighter_corner.xpath(".//div[@class='c-listing-fight__outcome--win']/text()").get()):
                r_fighter_status = 'loss'
                b_fighter_status = 'win'
            else:
                r_fighter_status = 'NC' 
                b_fighter_status = 'NC'



        fight = FightItem()
        fight["url"] = response.url 
        fight["r_fighter"] = r_fighter
        fight["b_fighter"] = b_fighter
        fight["r_fighter_status"] = r_fighter_status
        fight["b_fighter_status"] = b_fighter_status
        fight["round"] = round
        fight["time"] = time
        fight["method"] = method
        fight["bout_weight"] = bout_weight

        yield FightPipeline().process_item(fight, "")

