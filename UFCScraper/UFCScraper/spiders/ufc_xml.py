from scrapy.selector.unified import Selector
from scrapy.exceptions import CloseSpider
import scrapy
import re


class FightersSpider(scrapy.Spider):
    name = "ufc_xml"
    allowed_domains = ["www.ufc.com"]
    start_urls = ["https://www.ufc.com/sitemap.xml"]

    def parse(self, response):
        selector = Selector(text=response.text)

        urls = selector.xpath("//sitemap/loc/text()").extract()
        if urls == []:
            raise CloseSpider("No more pages to scrape")

        for url in urls:
            yield response.follow(url=url, callback=self.parse_urls)

    def parse_urls(self, response):
        selector = Selector(text=response.text)

        urls = selector.xpath("//url/loc/text()").extract()
        if urls == []:
            raise CloseSpider("No more pages to stcrape")

        for url in urls:
            # if "/athlete/" in url:
            #     yield response.follow(url=url, callback=self.parse_athletes)

            if "/event/" in url:
                yield response.follow(
                    url=url, callback=self.parse_events, meta={"url": url}
                )

    def parse_athletes(self, response):
        selector = Selector(text=response.text)

        name = selector.xpath("//h1[@class='hero-profile__name']/text()").get()
        nickname = selector.xpath("//p[@class='hero-profile__nickname']/text()").get()
        yield {"name": name, "nickname": nickname}

    def parse_events(self, response):
        selector = Selector(text=response.text)

        name_prefix = selector.xpath("//h1/text()").get().replace("\n", "").strip()

        name_suffix1 = (
            selector.xpath("//span[@class='e-divider__top']/text()")
            .get()
            .replace("\n", "")
            .strip()
        )
        name_suffix2 = (
            selector.xpath("//span[@class='e-divider__bottom']/text()")
            .get()
            .replace("\n", "")
            .strip()
        )

        name_complete = name_prefix + " " + name_suffix1 + " vs " + name_suffix2

        location = (
            selector.xpath(
                "//div[@class='field field--name-venue field--type-entity-reference field--label-hidden field__item']/text()"
            )
            .get()
            .replace("\n", "")
            .strip()
        )

        date_raw = (
            selector.xpath(
                "//div[@class='c-hero__headline-suffix tz-change-inner']/text()"
            )
            .get()
            .replace("\n", "")
            .strip()
        )

        yield {
            "name": name_complete,
            "location": location,
            "date": date_raw,
            "url": response.meta["url"],
        }
