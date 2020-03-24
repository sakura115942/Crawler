# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class YandeItem(scrapy.Item):
    image_id = scrapy.Field()
    image_url = scrapy.Field()
