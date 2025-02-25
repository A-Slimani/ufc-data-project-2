from UFCScraper.pipelines import EventPipeline, FighterPipeline
from UFCScraper.items import EventItem, FighterItem, FightItem
from scrapy.exceptions import CloseSpider
import scrapy
import json

class EventsApiSpider(scrapy.Spider):
    name = "ufc_events"
    allowed_domains = ["d29dxerjsp82wz.cloudfront.net"]   
    page_number = 1 
    err_count = 0 
    start_urls = [f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{page_number}.json"]

    handle_httpstatus_list = [502]

    custom_settings = {"ITEM_PIPELINES": {"UFCScraper.pipelines.EventPipeline": 300}}

    with open('missing_event_data.txt', 'w') as file:
        file.write("::: Missing event data pages :::\n")

    def parse(self, response):
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

        except KeyError:
            with open('missing_event_data.txt', 'a') as file:
                file.write(f"{self.page_number}\n")
            self.err_count += 1

        if self.err_count > 5:
            raise CloseSpider("End of pages")


        self.page_number += 1
        next_page = f"https://d29dxerjsp82wz.cloudfront.net/api/v3/event/live/{self.page_number}.json"
        yield response.follow(next_page, callback=self.parse)

