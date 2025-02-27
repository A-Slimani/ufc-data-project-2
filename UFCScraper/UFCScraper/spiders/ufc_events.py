from UFCScraper.pipelines import EventPipeline, FighterPipeline
from UFCScraper.items import EventItem, FighterItem, FightItem
from scrapy.exceptions import CloseSpider
import scrapy
import json

class EventsApiSpider(scrapy.Spider):
    name = "ufc_events"
    allowed_domains = ["d29dxerjsp82wz.cloudfront.net"]   
    start_page = 1 
    max_pages = 12000
    start_urls = [f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{start_page}.json"]

    handle_httpstatus_list = [502]

    custom_settings = {"ITEM_PIPELINES": {"UFCScraper.pipelines.EventPipeline": 300}}

    with open('missing_event_data.txt', 'w') as file:
        file.write("::: Missing event data pages :::\n")
    

    def parse(self, response):
        for page_no in range(self.start_page, self.max_pages):
            url = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{page_no}.json"
            yield response.follow(url, callback=self.parse_events, meta={"page_no": page_no})


    def parse_events(self, response):
        data = json.loads(response.body)
        event = EventItem()
        try:
            self.error_count = 0
            event_details = data["LiveEventDetail"]

            event["id"] = event_details["EventId"]
            event["name"] = event_details["Name"]
            event["date"] = event_details["StartTime"]
            event["city"] = event_details["Location"]["City"]
            event["state"] = event_details["Location"]["State"]
            event["country"] = event_details["Location"]["Country"]
            event["venue"] = event_details["Location"]["Venue"]

            yield event 

        except KeyError as e:
            with open('error_list_events.log', 'a') as file:
                file.write(f"{response.meta['page_no']} :: KeyError:{str(e)} \n")

        except Exception as e:
            with open('error_list_events.log', 'a') as file:
                file.write(f"{response.meta['page_no']} :: {str(e)} \n")


