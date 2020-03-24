# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy import Request
from scrapy.pipelines.files import FilesPipeline
import zipfile
import imageio
import os
import re
import shutil
# https://i.pximg.net/img-original/img/2019/12/23/00/18/37/78429594_p0.jpg


class PixivImagePipeline(FilesPipeline):

    def get_media_requests(self, item, info):
        meta = {'referer': item['referer'],
                'item': item}
        page_count = item['page_count']
        original_url = item['original_url']
        illust_type = item['illust_type']
        if illust_type == 2:
            yield Request(item['gif_zip_url'], meta=meta)
        if page_count == 1:
            yield Request(url=original_url, meta=meta)
        else:
            yield from [Request(original_url.replace('p0', 'p%d' % _), meta=meta) for _ in range(page_count)]

    def file_path(self, request, response=None, info=None):
        name = request.url.split('/')[-1]
        item = request.meta['item']
        return 'full/%s/%s' % (item['author'], name)

    def item_completed(self, results, item, info):
        if isinstance(item, dict) or self.files_result_field in item.fields:
            item[self.files_result_field] = [x for ok, x in results if ok]
        if item['illust_type'] == 2:
            file_paths = [x['path'] for ok, x in results if ok]
            base_path = 'full/%s' % item['author']
            unzip_path = base_path + '/%s' % item['author']
            output_path = file_paths[1].replace('jpg', 'gif')
            zFile = zipfile.ZipFile(file_paths[0], "r")
            frames = zFile.namelist()
            for fileM in zFile.namelist():
                zFile.extract(fileM, unzip_path)
            zFile.close()
            frames = [imageio.imread(unzip_path + '/%s' % image) for image in frames]
            imageio.mimsave(output_path, frames, 'GIF', duration=0)
            os.remove(file_paths[0])
            shutil.rmtree(unzip_path)
        return item


class ClearPipeline(object):

    def process_item(self, item, spider):
        item['description'] = re.sub(r'<[^>]*>', ' ', item['description']).replace('\n', ' ').replace('\u3000', ' ')
        return item














# class MySQLPipeline(object):
#     collection_name = 'yande_items'
#
#     def __init__(self, mongo_uri, mongo_db):
#         self.mongo_uri = mongo_uri
#         self.mongo_db = mongo_db
#
#     @classmethod
#     def from_crawler(cls, crawler):
#         return cls(
#             mongo_uri=crawler.settings.get('MONGO_URI'),
#             mongo_db=crawler.settings.get('MONGO_DATABASE')
#         )
#
#     def open_spider(self, spider):
#         self.client = pymongo.MongoClient(self.mongo_uri)
#         self.db = self.client[self.mongo_db]
#
#     def close_spider(self, spider):
#         self.client.close()
#
#     def process_item(self, item, spider):
#         self.db[self.collection_name].insert_one(dict(item))
#         return item