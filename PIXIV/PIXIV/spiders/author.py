# -*- coding: utf-8 -*-
import scrapy
from ..items import ArtworksItem
from ..temporary import cookie
import json
# https://i.pximg.net/img-zip-ugoira/img/2014/09/15/04/28/24/45988308_ugoira600x600.zip
# 如果是gif 调用api 获取 api response 后解析body 获得 gif zip
# https://www.pixiv.net/ajax/illust/45988308/ugoira_meta 的地址
cookies = dict([item.split("=", 1) for item in cookie.split("; ")])


class AuthorSpider(scrapy.Spider):
    name = 'author'
    allowed_domains = ['pixiv.net']

    def start_requests(self):
        user_id = getattr(self, 'user_id')
        url = f'https://www.pixiv.net/ajax/user/{user_id}/profile/all'
        yield scrapy.Request(url, callback=self.parse, cookies=cookies)

    def parse(self, response):
        data = json.loads(response.text)
        illusts = data['body']['illusts'].keys()
        manga = data['body']['manga'].keys()
        _all = list(illusts) + list(manga)
        _all = _all[:10]
        for artworks_id in _all:
            url = f'https://www.pixiv.net/artworks/{artworks_id}'
            yield scrapy.Request(url, callback=self.parse_artworks)
        # yield from [scrapy.Request('https://www.pixiv.net/artworks/{%s}' % _, callback=self.parse_artworks)for _ in _all]

    def parse_artworks(self, response):
        meta = json.loads(response.xpath('//meta[@id="meta-preload-data"]/@content').get())
        _ = meta['illust']
        detail = _[list(_)[0]]
        item = ArtworksItem()
        item['id'] = detail.get('id', None)
        item['title'] = detail.get('title', None)
        item['description'] = detail.get('description', None)
        item['author'] = detail.get('userName', None)
        tags = detail.get('userIllusts', None).get(item['id'], None).get('tags', None)
        item['tags'] = ' '.join(tags)
        item['illust_type'] = detail.get('illustType', None)
        item['create_date'] = detail.get('createDate', None)
        item['upload_date'] = detail.get('uploadDate', None)

        item['width'] = detail.get('width', None)
        item['height'] = detail.get('width', None)
        item['bookmark_count'] = detail.get('bookmarkCount', None)
        item['like_count'] = detail.get('likeCount', None)
        item['comment_count'] = detail.get('commentCount', None)
        item['view_count'] = detail.get('viewCount', None)

        item['referer'] = response.url
        urls = detail.get('urls', None)

        if urls is not None:
            item['thumb_url'] = urls.get('thumb', None)
            item['small_url'] = urls.get('small', None)
            item['regular_url'] = urls.get('regular', None)
            item['original_url'] = urls.get('original', None)
        item['page_count'] = detail.get('pageCount', None)

        if item['illust_type'] == 2:
            url = 'https://www.pixiv.net/ajax/illust/{}/ugoira_meta'.format(item['id'])
            yield scrapy.Request(url, callback=self.parse_gif, meta={'item': item})
        else:
            yield item

    def parse_gif(self, response):
        data = json.loads(response.text)
        gif_zip_url = data.get('body', None).get('originalSrc', None)
        item = response.meta['item']
        item['gif_zip_url'] = gif_zip_url
        yield item
