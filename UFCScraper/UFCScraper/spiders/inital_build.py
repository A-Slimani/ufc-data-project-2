from scrapy.selector.unified import Selector
from scrapy.exceptions import CloseSpider
from UFCScraper.items import EventItem, FighterItem
from UFCScraper.pipelines import EventPipeline, FighterPipeline
import scrapy


class FightersSpider(scrapy.Spider):
    name = "initial_build"
    allowed_domains = ["www.ufc.com"]
    start_urls = ["https://www.ufc.com/sitemap.xml"]

    def clean_text(self, text) -> str:
        return text.replace("\n", "").strip()

    def inches_to_cm(self, value):
        if value != "":
            return round(float(value) * 2.54)
        else:
            return None

    def parse(self, response):
        selector = Selector(text=response.text)

        urls = selector.xpath("//sitemap/loc/text()").extract()
        if urls == []:
            raise CloseSpider("No more pages to scrape")

        ## UNCOMMENT ONCE DONE TESTING
        for url in urls:
            yield response.follow(url=url, callback=self.parse_urls)

        # USE ONLY FOR TESTING
        # for x in range(2):
        #     yield response.follow(url=urls[x], callback=self.parse_urls)

    def parse_urls(self, response):
        selector = Selector(text=response.text)

        urls = selector.xpath("//url/loc/text()").extract()
        if urls == []:
            raise CloseSpider("No more pages to stcrape")

        for url in urls:
            ## UNCOMMENT ONCE DONE TESTING
            if "/athlete/" in url:
                yield response.follow(url=url, callback=self.parse_athletes)

            ## UNCOMMENT ONCE DONE TESTING
            if "/event/" in url:
                yield response.follow(url=url, callback=self.parse_events)

    def parse_athletes(self, response):
        selector = Selector(text=response.text)

        name = selector.xpath("//h1[@class='hero-profile__name']/text()").get()
        nickname = selector.xpath("//p[@class='hero-profile__nickname']/text()").get()
        record_raw = selector.xpath(
            "//p[@class='hero-profile__division-body']/text()"
        ).get()
        record_processed = (
            record_raw.split(" ")[0].split("-") if record_raw else [None, None, None]
        )
        wins = record_processed[0]
        losses = record_processed[1]
        draws = record_processed[2]

        weight_class_raw = selector.xpath(
            "//p[@class='hero-profile__division-title']/text()"
        ).get()
        weight_class_cleaned = (
            weight_class_raw.replace(" Division", "").strip()
            if weight_class_raw
            else None
        )

        bio_field = selector.xpath("//div[@class='c-bio__field']")
        paired_bio = []
        for bio in bio_field:
            bio_label = bio.xpath("div[@class='c-bio__label']/text()").get()
            bio_text = bio.xpath("div[@class='c-bio__text']/text()").get()
            if self.clean_text(bio_text) == "":
                bio_text = bio.xpath("div[@class='c-bio__text']/div/text()").get()
            paired_bio.append((bio_label, bio_text))
        bio_details = dict(paired_bio)

        hometown = None
        try:
            if "Status" in bio_details:
                hometown_element = selector.xpath(
                    "//div[@class='c-bio__row--1col']/div/div[@class='c-bio__text']/text()"
                ).getall()
                if len(hometown_element) > 1:
                    hometown = hometown_element[1]
                else:
                    hometown = hometown_element[0]

            else:
                hometown = selector.xpath(
                    "//div[@class='c-bio__row--1col']/div/div[@class='c-bio__text']/text()"
                ).get()
        except:
            print(f"Missing hometown data for: {name}")

        row_2col = selector.xpath("//div[@class='c-bio__row--2col']")
        values = []
        fields = row_2col.xpath("//div[@class='c-bio__row--2col']/div[@class='c-bio__field c-bio__field--border-bottom-small-screens']")
        for field in fields:
            label = field.xpath("div[@class='c-bio__label']/text()").get()
            text = field.xpath("div[@class='c-bio__text']/text()").get()
            values.append((label, text))
        values_dict = dict(values)

        fighter = FighterItem()
        fighter["name"] = name
        fighter["nickname"] = nickname
        fighter["status"] = bio_details["Status"] if "Status" in bio_details else None
        fighter["record_raw"] = record_raw
        fighter["wins"] = wins
        fighter["losses"] = losses
        fighter["draws"] = draws
        fighter["weight_class"] = weight_class_cleaned
        fighter["age"] = bio_details["Age"] if "Age" in bio_details else None
        fighter["height"] = (
            self.inches_to_cm(bio_details["Height"])
            if "Height" in bio_details
            else None
        )
        fighter["reach"] = (
            self.inches_to_cm(bio_details["Reach"]) if "Reach" in bio_details else None
        )
        fighter["leg_reach"] = (
            self.inches_to_cm(bio_details["Leg reach"])
            if "Leg reach" in bio_details
            else None
        )
        fighter["hometown"] = hometown
        fighter["trains_at"] = values_dict["Trains at"] if "Trains at" in values_dict else None
        fighter["fighting_style"] = values_dict["Fighting style"] if "Fighting style" in values_dict else None
        fighter["url"] = response.url

        yield FighterPipeline().process_item(fighter, "")

    def parse_events(self, response):
        selector = Selector(text=response.text)

        try:
            name_prefix = self.clean_text(selector.xpath("//h1/text()").get())
        except:
            name_prefix = ""

        try:
            name_suffix1 = self.clean_text(
                selector.xpath("//span[@class='e-divider__top']/text()").get()
            )
        except:
            name_suffix1 = ""

        try:
            name_suffix2 = self.clean_text(
                selector.xpath("//span[@class='e-divider__bottom']/text()").get()
            )
        except:
            name_suffix2 = ""

        if name_suffix1 == "" or name_suffix2 == "":
            name_complete = name_prefix
        else:
            name_complete = name_prefix + " " + name_suffix1 + " vs " + name_suffix2

        try:
            location_raw = self.clean_text(
                selector.xpath(
                    "//div[@class='field field--name-venue field--type-entity-reference field--label-hidden field__item']/text()"
                ).get()
            )
        except:
            location_raw = ""

        try:
            date_raw = self.clean_text(
                selector.xpath(
                    "//div[@class='c-hero__headline-suffix tz-change-inner']/text()"
                ).get()
            )
        except:
            date_raw = ""

        event = EventItem()
        event["name"] = name_complete
        event["location_raw"] = location_raw
        event["date_raw"] = date_raw
        event["url"] = response.url

        yield EventPipeline().process_item(event, "")
