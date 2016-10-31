import scrapy


class ListSpider(scrapy.Spider):
    name = 'listspider'
    start_urls = ['http://localhost:3000']

    def parse(self, response):
        for link in response.css('.content div'):
            href = link.css('a::attr("href")').extract_first()
            yield scrapy.Request(response.urljoin(href), self.parse_job)
        next_page = response.css('.next a::attr("href")').extract_first()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, self.parse)

    def parse_job(self, response):
        yield {
            'content': response.css('.description::text').extract_first()
        }

