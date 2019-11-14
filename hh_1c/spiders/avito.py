# -*- coding: utf-8 -*-
import scrapy


class AvitoSpider(scrapy.Spider):
    name = 'avito'
    allowed_domains = ['avito.ru']
    start_urls = ['https://www.avito.ru/rossiya/kvartiry']

    def parse(self, response):

        pagination = response.xpath('//div[contains(@class, "pagination")]/'
            'div[contains(@class, "pagination-nav")]/a[contains(@class, "js-pagination-next")]/@href').extract_first()

        next_link = pagination
        yield response.follow(next_link, callback=self.parse)

        kvartiry_pages = response.xpath('//div[contains(@class, "catalog_table")]'
            '//div[contains(@class, "item")]'
            '//h3[@data-marker="item-title"]/a/@href').extract()

        for kvartira in kvartiry_pages:
            yield response.follow(kvartira, callback=self.parse_kvartira_page)
        pass

    def parse_kvartira_page(self, response):
        #Название,
        title = response.xpath('//h1[@class="title-info-title"]/span[@itemprop="name"]/text()').extract_first()

        # Ссылки на все фото,
        photos = response.xpath('//div[contains(@class, "js-gallery-img-frame")]/@data-url').extract()

        # Стоимость,
        price = response.xpath('//div[@class="item-price"]//span[@class="js-item-price"]/@content').extract_first()

        # URL объявления,
        kvartira_url = response.url

        # URL автора объявления,
        author_url = response.xpath('//div[@class="seller-info-value"]//a/@href').extract_first()
        # Адрес местоположения объекта
        location = response.xpath('//div[@class="item-address"]/span/text()').extract_first()


        item = {
            'title': title,
            'photos': photos,
            'price': price,
            'kvartira_url': kvartira_url,
            'author_url': author_url,
            'location': location
            }

        yield item
        print(1)