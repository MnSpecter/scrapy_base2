import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient


class DataBasePipeline(object):
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongo_base = client.leroy_photo

    def process_item(self, item, spider):
        new_item = {
            'Название': item['name'],
            'Фото': item['photos'],
            'Цена': item['price'],
            'Описание': item['about'],
        }
        for char in item['chars'][0]:
            new_item[char] = item['chars'][0][char]

        print(f'\nВносим элемент в БД:')
        print(new_item)

        collection = self.mongo_base[spider.name]
        collection.insert_one(new_item)
        return new_item

class PhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        print(info)
        if item['photos']:
            for img in item['photos']:
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [itm[1] for itm in results if itm[0]]
        return item
