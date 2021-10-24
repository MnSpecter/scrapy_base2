import scrapy
from scrapy.http import HtmlResponse

from jobparser.items import AvitoparserItem


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://www.avito.ru/rossiya/bytovaya_elektronika?q={mark}']

    def parse(self, response: HtmlResponse):
        ads_links = response.xpath('//div[@data-marker="item"]//a[@class="iva-item-sliderLink-bJ9Pv"]'
                                   '//@href').extract()
        for link in ads_links:
            yield response.follow('https://www.avito.ru' + link, callback=self.parse_ads)

    def parse_ads(self, response: HtmlResponse):
        name = response.xpath('//span[@class="title-info-title-text"]//text()').extract()
        photos = response.xpath('//div[contains(@class , "gallery-img-wrapper")]'
                                '//div[contains(@class, "gallery-img-frame")]/@data-url').extract()
        price = response.xpath('//span[@class="js-item-price"]//text()').getall()
        print(name[0])
        print(photos)

        yield AvitoparserItem(name=name, photos=photos, price=price)
