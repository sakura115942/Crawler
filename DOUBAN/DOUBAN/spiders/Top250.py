# -*- coding: utf-8 -*-
import scrapy
from DOUBAN.items import DoubanItem
#scrapy shell -s USER_AGENT="Mozilla" "https://movie.douban.com/top250"


class Top250Spider(scrapy.Spider):
    name = 'Top250'
    allowed_domains = ['douban.com']
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        next_page = response.xpath('//span[@class="next"]/a/@href').get()
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)
        info = response.xpath('//div[@class="info"]')
        for each in info:
            item = DoubanItem()
            item['title'] = each.xpath('div[@class="hd"]/a/span/text()').get()
            item['rating_num'] = each.xpath('.//span[@class="rating_num"]/text()').get()
            item['quote'] = each.xpath('.//span[@class="inq"]/text()').get()
            yield item
