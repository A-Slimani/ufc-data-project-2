# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

def inches_to_cm(value):
    return round(value * 2.54)


class FighterItem(scrapy.Item):
    name = scrapy.Field()
    status = scrapy.Field()
    nickname = scrapy.Field()
    weight_class = scrapy.Field()
    age = scrapy.Field()
    hometown = scrapy.Field()
    trains_at = scrapy.Field()
    fighting_style = scrapy.Field()
    height = scrapy.Field(input_processor=inches_to_cm)
    reach = scrapy.Field()
    debut_date = scrapy.Field()
    wins = scrapy.Field()
    losses = scrapy.Field()
    draws = scrapy.Field()
    wins_by_ko_tko = scrapy.Field()
    wins_by_sub = scrapy.Field()
    wins_by_dec = scrapy.Field()
