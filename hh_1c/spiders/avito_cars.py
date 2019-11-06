# -*- coding: utf-8 -*-
import scrapy
import json
from scrapy.http import HtmlResponse
from scrapy.loader import ItemLoader

from hh_1c.items import AvitoCar

class AvitoCarsSpider(scrapy.Spider):
    name = 'avito_cars'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/avtomobili']

    def parse(self, response):

        pagination = response.xpath('//div[contains(@class, "pagination")]/'
            'div[contains(@class, "pagination-nav")]/a[contains(@class, "js-pagination-next")]/@href').extract_first()

        next_link = pagination
        yield response.follow(next_link, callback=self.parse)

        cars_pages = response.xpath('//div[contains(@class, "catalog_table")]'
            '//div[contains(@class, "item")]'
            '//h3[@data-marker="item-title"]/a/@href').extract()

        for car in cars_pages:
            yield response.follow(car, callback=self.parse_car_page)
        pass

    def parse_car_page(self, response):

        # URL объявления,
        car_url = response.url

        # URL автора объявления,
        author_url = response.xpath('//div[@class="seller-info-value"]//a/@href').extract_first()
        # Адрес местоположения объекта
        location = response.xpath('//div[@class="item-address"]/span/text()').extract_first()


        item = ItemLoader(AvitoCar(), response)

        # Заголовок
        item.add_xpath('title', '//h1[@class="title-info-title"]/span[@itemprop="name"]/text()')
        # Цена
        item.add_xpath('price', '//div[@class="item-price"]//span[@class="js-item-price"]/@content')
        # Фото
        item.add_xpath('photos', '//div[contains(@class, "js-gallery-img-frame")]/@data-url')
        # характеристики
        item.add_xpath('params', '//div[@class="item-params"]/ul[@class="item-params-list"]/li')

        # Данные по VIN
        autoteka_id = response.xpath('//div[@class="js-autoteka-teaser"]/@data-item-id').extract_first()
        autoteka_url = f'https://www.avito.ru/web/1/swaha/v1/autoteka/teaser/{autoteka_id}?unlockCrashes=false'

        #autoteka_url = 'https://autoteka.ru/report_by_ad/1808335001?utm_source=avito.ru&utm_medium=referral&utm_campaign=teaser'

        yield scrapy.Request(url=autoteka_url,
                             callback=self.parse_addparams, dont_filter=True, cb_kwargs={'item': item})

        # Подробные характеристики - не сделано

        #yield item.load_item()


    def parse_addparams(self, response:HtmlResponse, item):

        item.add_value('add_params', json.loads(response.body))
        #yield item
        yield item.load_item()
        pass