from UFCScraper.items import FighterItem
from scrapy.exceptions import CloseSpider
import scrapy
import json

class EventsApiSpider(scrapy.Spider):
    name = "ufc_fighters"
    allowed_domains = ["d29dxerjsp82wz.cloudfront.net"]   
    page_number = 1 
    err_count = 0 
    start_urls = [f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{page_number}.json"]

    handle_httpstatus_list = [502]

    custom_settings = {"ITEM_PIPELINES": {"UFCScraper.pipelines.FighterPipeline": 400}}

    with open('missing_event_data.txt', 'w') as file:
        file.write("::: Missing event data pages :::\n")

    def parse(self, response):
        data = json.loads(response.body)
        try:
            self.error_count = 0
            event_details = data["LiveEventDetail"]

            # add the fighter first then the fights
            fighter_item = FighterItem()
            for fight in event_details['FightCard']:
                for fighter in fight['Fighters']: 
                    fighter_item['id'] = fighter['FighterId']
                    fighter_item['first_name'] = fighter['Name']['FirstName']
                    fighter_item['last_name'] = fighter['Name']['LastName']
                    fighter_item['nickname'] = fighter['Name']['NickName']
                    fighter_item['hometown_city'] = fighter['Born']['City']
                    fighter_item['hometown_state'] = fighter['Born']['State']
                    fighter_item['hometown_country'] = fighter['Born']['Country']
                    fighter_item['trains_at_city'] = fighter['FightingOutOf']['City']
                    fighter_item['trains_at_state'] = fighter['FightingOutOf']['State']
                    fighter_item['trains_at_country'] = fighter['FightingOutOf']['Country']
                    fighter_item['wins'] = fighter['Record']['Wins']
                    fighter_item['losses'] = fighter['Record']['Losses']
                    fighter_item['draws'] = fighter['Record']['Draws']
                    fighter_item['age'] = fighter['Age']
                    fighter_item['height'] = fighter['Height']
                    fighter_item['stance'] = fighter['Stance']
                    fighter_item['reach'] = fighter['Reach']
                    fighter_item['url'] = fighter['UFCLink']

                    yield fighter_item 

        except KeyError:
            with open('missing_event_data.txt', 'a') as file:
                file.write(f"{self.page_number}\n")
            self.err_count += 1

        if self.err_count > 5:
            raise CloseSpider("End of pages")


        self.page_number += 1
        next_page = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{self.page_number}.json"
        yield response.follow(next_page, callback=self.parse)

