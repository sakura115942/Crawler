# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class ArtworksItem(scrapy.Item):
    id = scrapy.Field()              # 插画 id
    title = scrapy.Field()
    description = scrapy.Field()     # 描述
    illust_type = scrapy.Field()     # 插画 类型 0：插画 1：漫画 2：gif
    author = scrapy.Field()
    tags = scrapy.Field()

    create_date = scrapy.Field()
    upload_date = scrapy.Field()

    width = scrapy.Field()
    height = scrapy.Field()
    bookmark_count = scrapy.Field()  # 收藏
    like_count = scrapy.Field()      # 赞
    comment_count = scrapy.Field()   # 评论数量
    view_count = scrapy.Field()      # 浏览量

    referer = scrapy.Field()

    thumb_url = scrapy.Field()       # 插画各种尺寸链接
    small_url = scrapy.Field()
    regular_url = scrapy.Field()
    original_url = scrapy.Field()

    page_count = scrapy.Field()      # 插画张数
    gif_zip_url = scrapy.Field()     # gif图包地址
