import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
import html


class Job(scrapy.Item):
    url = scrapy.Field()
    title = scrapy.Field()
    description = scrapy.Field()
    time = scrapy.Field()
    salary = scrapy.Field()
    location = scrapy.Field()


class ReedSpider(CrawlSpider):
    name = "reed"
    allowed_domains = ["reed.co.uk"]
    start_urls = ['https://www.reed.co.uk/jobs']

    rules = [
        Rule(
            LinkExtractor(
                restrict_css=('.results .job-result .job-block-link')
            ),
            callback='parse_item',
        ),
        Rule(
            LinkExtractor(
                restrict_css=('.pages .page[title="Go to next page"]')
            ),
            follow=True
        ),
    ]

    def parse_item(self, response):
        def extract_and_sanitize(selector):
            return html.unescape(
                BeautifulSoup(
                    response.css(selector).extract()[0]
                ).get_text().strip().replace('\n', ' ')
            )

        item = Job()
        item['url'] = response.url
        item['title'] = extract_and_sanitize('.description-container .job-header h1')
        description = ''
        for element in response.xpath('//*[@class="description"]/node()[position()>2]').extract():
            description = description + ' ' + html.unescape(BeautifulSoup(element).get_text().strip().replace('\n', ' '))
        item['description'] = description.strip()
        item['location'] = extract_and_sanitize('.description-container .location')
        item['time'] = extract_and_sanitize('.description-container .time')
        item['salary'] = extract_and_sanitize('.description-container .salary')
        return item
