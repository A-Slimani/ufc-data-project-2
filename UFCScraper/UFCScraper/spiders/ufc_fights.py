from UFCScraper.items import FightItem
import scrapy
import json

class FightsApiSpider(scrapy.Spider):
    name = "ufc_fights"
    allowed_domains = ["d29dxerjsp82wz.cloudfront.net"]
    start_page = 30 
    max_pages = 12000 
    err_page_list = []
    start_urls = [f"https://d29dxerjsp82wz.cloudfront.net/api/v3/fight/live/{start_page}.json"]

    handle_httpstatus_list = [502]

    custom_settings = {"ITEM_PIPELINES": {"UFCScraper.pipelines.FightPipeline": 200}}

    with open('missing_fight_data.txt', 'w') as file:
        file.write("::: Missing event data pages :::\n")
    
    def parse(self, response):
        for page_no in range(self.start_page, self.max_pages):
            url = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/fight/live/{page_no}.json"
            yield response.follow(url, callback=self.parse_fights, meta={"page_no": page_no})

    
    def parse_fights(self, response):
        data = json.loads(response.body)
        try:
            self.error_count = 0
            fight = data["LiveFightDetail"]

            fight_item = FightItem()
            fight_item['id'] = fight['FightId']
            fight_item['event_id'] = fight['Event']['EventId'] # foreign key
            fight_item['r_fighter_id'] = fight['Fighters'][0]['FighterId'] # foreign key
            fight_item['b_fighter_id'] = fight['Fighters'][1]['FighterId'] # foreign key
            fight_item['r_fighter_status'] = fight['Fighters'][0]['Outcome']['Outcome']
            fight_item['b_fighter_status'] = fight['Fighters'][1]['Outcome']['Outcome']
            fight_item['round'] = fight['Result']['EndingRound']
            fight_item['time'] = fight['Result']['EndingTime']
            fight_item['method'] = fight['Result']['Method']
            fight_item['bout_weight'] = fight['WeightClass']['Description']
            fight_item['url'] = response.url
            fight_item['fight_stats'] = fight['FightStats']
            yield fight_item
        
        except KeyError as e:
            with open('error_list_fights.log', 'a') as file:
                file.write(f"{response.meta['page_no']} :: KeyError:{str(e)} \n")

        except Exception as e:
            with open('error_list_fights.log', 'a') as file:
                file.write(f"{response.meta['page_no']} :: {str(e)} \n")
        
