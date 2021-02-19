import scrapy

from scrapy.loader import ItemLoader
from ..items import CaceisItem
from itemloaders.processors import TakeFirst


class CaceisSpider(scrapy.Spider):
	name = 'caceis'
	start_urls = ['https://www.caceis.com/whats-new/']

	def parse(self, response):
		post_links = response.xpath('//div[@class="header"]/h3/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//article//text()[normalize-space() and not(ancestor::p[@class="news-img-caption"] | ancestor::div[@class="footer date"] | ancestor::a[@href="/whats-new/news/"] | ancestor::div[@class="news-related-wrap"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//span[@class="page-title-date"]//text()').get()

		item = ItemLoader(item=CaceisItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
