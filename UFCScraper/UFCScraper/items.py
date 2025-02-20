from scrapy.loader import ItemLoader
import scrapy


class FighterItem(scrapy.Item):
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
    url = scrapy.Field(required=True)


class EventItem(scrapy.Item):
    name = scrapy.Field()
    location_raw = scrapy.Field()
    date_raw = scrapy.Field()
    url = scrapy.Field(required=True)
