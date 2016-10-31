# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

class Job(scrapy.Item):
    description = scrapy.Field()

class LocalhostSpider(CrawlSpider):
    name = "localhost"
    allowed_domains = ["localhost"]
    start_urls = ['http://localhost:3000/index.html']

    rules = [
        Rule(
            LinkExtractor(
                restrict_css=('.content div a')
            ),
            callback='parse_item',
        ),
        Rule(
            LinkExtractor(
                restrict_css=('.next a')
            ),
            follow=True
        ),
    ]

    # def parse(self, response):
    #     next_page = response.css('.next a::attr("href")').extract_first()
    #     if next_page is not None:
    #         next_page = response.urljoin(next_page)
    #         yield scrapy.Request(next_page, self.parse)

    def parse_item(self, response):
        def extract_and_sanitize(selector):
            return BeautifulSoup(response.css(selector).extract()[0]).get_text().strip().replace('\n', ' ')

        item = Job()
        description = ''
        for element in response.css('.description div').extract():
            description = description + BeautifulSoup(element).get_text().strip().replace('\n', ' ')
        item['description'] = description
        return item
