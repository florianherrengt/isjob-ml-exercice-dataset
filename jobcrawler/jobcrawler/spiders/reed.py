import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup


class Job(scrapy.Item):
    title = scrapy.Field()
    description = scrapy.Field()


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
            return BeautifulSoup(response.css(selector).extract()[0]).get_text().strip().replace('\n', ' ')

        item = Job()
        item['title'] = extract_and_sanitize('.description-container .job-header h1')
        print(response.css('.description'))
        description = ''
        for element in response.xpath('//*[@class="description"]/node()[position()>2]').extract():
            description = description + ' ' + BeautifulSoup(element).get_text().strip().replace('\n', ' ')
        item['description'] = description.strip()
        return item
