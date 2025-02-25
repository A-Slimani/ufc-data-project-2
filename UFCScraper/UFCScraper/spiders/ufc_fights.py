from UFCScraper.items import FightItem
from scrapy.exceptions import CloseSpider
import scrapy
import json

class FightsApiSpider(scrapy.Spider):
    name = "ufc_fights"
    allowed_domains = ["d29dxerjsp82wz.cloudfront.net"]
    page_number = 30 
    err_count = 0
    start_urls = [f"https://d29dxerjsp82wz.cloudfront.net/api/v3/fight/live/{page_number}.json"]

    handle_httpstatus_list = [502]

    custom_settings = {"ITEM_PIPELINES": {"UFCScraper.pipelines.FightPipeline": 200}}

    with open('missing_fight_data.txt', 'w') as file:
        file.write("::: Missing event data pages :::\n")
    
    def parse(self, response):
        data = json.loads(response.body)
        try:
            self.error_count = 0
            fight_details = data["LiveFightDetail"]

            fight_item = FightItem()
            for fight in fight_details:
                fight_item['fight_id'] = fight['Event']['FightId']
                fight_item['event_id'] = fight['EventId'] # foreign key
                fight_item['r_fighter_id'] = fight['Fighters'][0]['FighterId'] # foreign key
                fight_item['b_fighter_id'] = fight['Fighters'][1]['FighterId'] # foreign key
                fight_item['r_fighter_status'] = fight['Fighters'][0]['Outcome']['Outcome']
                fight_item['b_fighter_status'] = fight['Fighters'][1]['Outcome']['Outcome']
                fight_item['bout_weight'] = fight['WeightClass']['Description']
                fight_item['method'] = fight['Result']['Method']
                fight_item['round'] = fight['Result']['EndingRound']
                fight_item['time'] = fight['Result']['Time']
                fight_item['fight_stats'] = fight['FightStats']
                yield fight_item
        except KeyError:
            pass
