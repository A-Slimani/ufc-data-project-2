from scrapy.selector.unified import Selector
from scrapy.exceptions import CloseSpider
import scrapy
import re


class FightersSpider(scrapy.Spider):
    name = "ufc_xml"
    allowed_domains = ["www.ufc.com"]
    start_urls = ["https://www.ufc.com/sitemap.xml"]

    def clean_text(self, text) -> str:
        return text.replace("\n", "").strip()

    def parse(self, response):
        selector = Selector(text=response.text)

        urls = selector.xpath("//sitemap/loc/text()").extract()
        if urls == []:
            raise CloseSpider("No more pages to scrape")

        ## UNCOMMENT ONCE DONE TESTING
        # for url in urls:
        #     yield response.follow(url=url, callback=self.parse_urls)

        yield response.follow(url=urls[0], callback=self.parse_urls)   

    def parse_urls(self, response):
        selector = Selector(text=response.text)

        urls = selector.xpath("//url/loc/text()").extract()
        if urls == []:
            raise CloseSpider("No more pages to stcrape")

        for url in urls:
            if "/athlete/" in url:
                yield response.follow(url=url, callback=self.parse_athletes, meta={"url": url})

            ## UNCOMMENT ONCE DONE TESTING
            # if "/event/" in url:
            #     yield response.follow(
            #         url=url, callback=self.parse_events, meta={"url": url}
            #     )

    def parse_athletes(self, response):
        selector = Selector(text=response.text)

        name = selector.xpath("//h1[@class='hero-profile__name']/text()").get()
        nickname = selector.xpath("//p[@class='hero-profile__nickname']/text()").get()
        record_raw = selector.xpath("//p[@class='hero-profile__division-body']/text()").get()

        weight_class_raw = selector.xpath("//p[@class='hero-profile__division-title']/text()").get()
        weight_class_cleaned = weight_class_raw.replace(" Division", "").strip()

        bio_field = selector.xpath("//div[@class='c-bio__field']")
        paired_bio = []
        for bio in bio_field:
            bio_label = bio.xpath("div[@class='c-bio__label']/text()").get()
            bio_text = bio.xpath("div[@class='c-bio__text']/text()").get()
            if self.clean_text(bio_text) == "":
                bio_text = bio.xpath("div[@class='c-bio__text']/div/text()").get()
            paired_bio.append((bio_label, bio_text))
                
        # paired_bio = zip(bio_label, bio_text)

        yield {
            "name": name, 
            "nickname": nickname,
            "record_raw": record_raw,
            "weight_class": weight_class_cleaned,
            "bio": dict(paired_bio),
            "url": response.meta["url"],
            "url2": response.url
        }

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
            location = self.clean_text(
                selector.xpath(
                    "//div[@class='field field--name-venue field--type-entity-reference field--label-hidden field__item']/text()"
                ).get()
            )
        except:
            location = ""

        try:
            date_raw = self.clean_text(
                selector.xpath(
                    "//div[@class='c-hero__headline-suffix tz-change-inner']/text()"
                ).get()
            )
        except:
            date_raw = ""

        yield {
            "name": name_complete,
            "location_raw": location,
            "date_raw": date_raw,
            "url": response.meta["url"],
        }
