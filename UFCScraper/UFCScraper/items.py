from scrapy.loader import ItemLoader
import scrapy


class FighterItem(scrapy.Item):
    url = scrapy.Field(required=True)
    name = scrapy.Field()
    status = scrapy.Field()
    nickname = scrapy.Field()
    record_raw = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    draws = scrapy.Field()
    weight_class = scrapy.Field()
    age = scrapy.Field()
    height = scrapy.Field()
    reach = scrapy.Field()
    leg_reach = scrapy.Field()
    hometown = scrapy.Field()
    trains_at = scrapy.Field()
    fighting_style = scrapy.Field()


class EventItem(scrapy.Item):
    url = scrapy.Field(required=True)
    name = scrapy.Field()
    location_raw = scrapy.Field()
    date_raw = scrapy.Field()

class FightItem(scrapy.Item):
    url = scrapy.Field(required=True)
    r_fighter = scrapy.Field()
    b_fighter = scrapy.Field()
    r_fighter_status = scrapy.Field()   
    b_fighter_status = scrapy.Field()   
    round = scrapy.Field()
    time = scrapy.Field() 
    method = scrapy.Field()
    bout_weight = scrapy.Field()

