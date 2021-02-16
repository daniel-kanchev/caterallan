import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from caterallan.items import Article


class CaterSpider(scrapy.Spider):
    name = 'cater'
    start_urls = ['https://www.caterallen.co.uk/news/']

    def parse(self, response):
        heading = response.xpath('//a[@class="btn btnTertiary"]/@href').get()
        yield response.follow(heading, self.parse_article)

        links = response.xpath('//a[@class=" newsItem"]/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2[@class="newsHeaderTitle"]/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="newsHeaderDate"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="newsMain"]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
