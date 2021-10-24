import scrapy
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader
from jobparser.items import LeroyParserItem


class LeroySpider(scrapy.Spider):
    name = 'leroy'
    allowed_domains = ['leroymerlin.ru']

    def __init__(self, mark):
        self.start_urls = [f'https://leroymerlin.ru/catalogue/{mark}']

    def parse(self, response: HtmlResponse):
        next_page = 'https://leroymerlin.ru' \
                    + response.css('a[data-qa-pagination-item="right"]').attrib['href']
        response.follow(next_page, callback=self.parse)

        ads_links = response.css(
            'a[data-qa="product-name"]::attr(href)'
        ).extract()

        for link in ads_links:
            yield response.follow('https://leroymerlin.ru' + link, callback=self.parse_ads)

        if next_page:
            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

    def parse_ads(self, response: HtmlResponse):
        name = response.xpath('//h1[@slot="title"]//text()').extract()
        photos = response.xpath('//img[@itemprop="image"]//@src').extract()
        price = response.xpath('//span[@slot="price"]//text()').get()
        about = response.xpath(
            '//uc-pdp-section-layout//uc-pdp-section-vlimited[@class="section__vlimit"]'
            '//div[not(contains(@class,"def-list__group"))]'
        ).get()
        # словарь из всех параметров
        keys = response.xpath('//div[@class="def-list__group"]//dt//text()').getall()
        values = response.xpath('//div[@class="def-list__group"]//dd//text()').getall()
        clear_values = [x.replace('\n', '').strip() for x in values]
        chars = dict(zip(keys, clear_values))

        loader = ItemLoader(LeroyParserItem())
        loader.add_value('name', name)
        loader.add_value('photos', photos)
        loader.add_value('price', price)
        loader.add_value('about', about)
        loader.add_value('chars', chars)
        yield loader.load_item()

