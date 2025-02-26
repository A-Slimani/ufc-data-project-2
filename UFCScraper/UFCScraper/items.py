from itemloaders.processors import MapCompose
from scrapy.loader import ItemLoader
import scrapy


class FighterItem(scrapy.Item):
    id = scrapy.Field(input_processor=MapCompose(int))
    first_name = scrapy.Field()
    last_name = scrapy.Field()
    nickname = scrapy.Field()
    status = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    draws = scrapy.Field()
    weight_class = scrapy.Field()
    age = scrapy.Field()
    height = scrapy.Field()
    reach = scrapy.Field()
    leg_reach = scrapy.Field()
    hometown_city = scrapy.Field()
    hometown_state = scrapy.Field()
    hometown_country = scrapy.Field()
    trains_at_city = scrapy.Field()
    trains_at_state = scrapy.Field()
    trains_at_country = scrapy.Field()
    fighting_style = scrapy.Field()
    stance = scrapy.Field()
    url = scrapy.Field()


class EventItem(scrapy.Item):
    id = scrapy.Field(input_processor=MapCompose(int))
    name = scrapy.Field()
    date = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    country = scrapy.Field()   
    venue = scrapy.Field()


class FightItem(scrapy.Item):
    id = scrapy.Field(input_processor=MapCompose(int))
    event_id = scrapy.Field(input_processor=MapCompose(int))
    r_fighter_id = scrapy.Field(input_processor=MapCompose(int))
    b_fighter_id = scrapy.Field(input_processor=MapCompose(int))
    r_fighter_status = scrapy.Field()   
    b_fighter_status = scrapy.Field()   
    round = scrapy.Field(input_processor=MapCompose(int))
    time = scrapy.Field() 
    method = scrapy.Field()
    bout_weight = scrapy.Field()
    url = scrapy.Field()
    fight_stats = scrapy.Field()

