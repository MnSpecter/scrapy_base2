import scrapy
from itemloaders.processors import Join, MapCompose, TakeFirst
from w3lib.html import remove_tags

def filter_price(value):
    if value.isdigit():
        return value

class AvitoparserItem(scrapy.Item):
    # define the fields for your item here like:
    _id = scrapy.Field()
    name = scrapy.Field()
    photos = scrapy.Field()
    price = scrapy.Field()
    pass

class LeroyParserItem(scrapy.Item):

    # define the fields for your item here like:
    _id = scrapy.Field()

    name = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    about = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=Join(),
    )
    price = scrapy.Field(
        input_processor=MapCompose(filter_price),
        output_processor=TakeFirst(),
    )
    photos = scrapy.Field()
    chars = scrapy.Field()

    pass
