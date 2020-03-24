# -*- coding: utf-8 -*-
import scrapy
from YANDE.items import YandeItem


class YandeSpider(scrapy.Spider):
    name = 'yande'
    allowed_domains = ['yande.re']

    def start_requests(self):
        tags = getattr(self, 'tags')
        url = f'https://yande.re/post?tags={tags}'
        yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        next_page = response.xpath('//a[@class="next_page"]/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        image_urls = response.xpath('//a[@class="thumb"]/@href').getall()
        yield from [response.follow(_, callback=self.parse_image) for _ in image_urls]

    def parse_image(self, response):
        item = YandeItem()
        item['image_id'] = response.xpath('//div[@id="stats"]/ul/li/text()').re(r'Id: (\d+)')[0]
        item['image_url'] = response.xpath('//div[@class="content"]/div/img/@src').get()
        yield item
