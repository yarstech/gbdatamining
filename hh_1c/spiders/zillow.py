# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode, urljoin
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from scrapy.loader import ItemLoader
from hh_1c.items import Zillow

class ZillowSpider(scrapy.Spider):
    name = 'zillow'
    allowed_domains = ['zillow.com']
    start_urls = ['http://zillow.com/homes/']

    browser = webdriver.Firefox()
    #browser = webdriver.Safari()

    def __init__(self, cities, *args, **kwargs):
        self.cities = cities
        super().__init__(*args, **kwargs)



    def parse(self, response):

        for city in self.cities:
            yield response.follow(urljoin(self.start_urls[0], city),
                                  callback=self.parse_city,
                                  cb_kwargs={'city': city})

    def parse_city(self, response, city):

        next = response.css('.zsg-pagination-next a::attr(href)').extract_first()

        yield response.follow(next, callback=self.parse_city,
                                  cb_kwargs={'city': city})
        real_estate_list = response.css(
            'div#grid-search-results ul.photo-cards li article a.list-card-link::attr(href)'
        )
        for adv in real_estate_list.extract():
            yield response.follow(adv, callback=self.parse_adv)

        print(1)

    def parse_adv(self, response):
        self.browser.get(response.url)
        media = self.browser.find_element_by_css_selector('.ds-media-col')
        #self.browser.find_element_by_xpath('//div[@class="sc-Rmtcm jEcXig"]')
        photo_pic_img_len = len(self.browser.find_elements_by_xpath(
            '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))


        while True:
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            media.send_keys(Keys.PAGE_DOWN)
            time.sleep(2)

            tmp_len = len(self.browser.find_elements_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))

            if photo_pic_img_len == tmp_len:
                break

            photo_pic_img_len = len(self.browser.find_elements_by_xpath(
                '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]'))

        #Все фото


        images = [itm.get_attribute('srcset').split(' ')[-2] for itm in
                  self.browser.find_elements_by_xpath(
                      '//ul[@class="media-stream"]/li/picture/source[@type="image/jpeg"]')
                  ]

        #Заголовок
        title = self.browser.find_elements_by_xpath(
            '//div[@data-test-id="bdp-building-info"]/h1[@data-test-id="bdp-building-title"]')

        # Параметры недвижимости
        param_names = self.browser.find_elements_by_xpath(
            '//ul[@class="ds-home-fact-list"]/li/span[@class="ds-standard-label ds-home-fact-label"]')
        param_values = self.browser.find_elements_by_xpath(
            '//ul[@class="ds-home-fact-list"]/li/span[@class="ds-body ds-home-fact-value"]')

        params = {}

        for i in range(0, len(param_names)):
            params[param_names[i].text]=param_values[i].text


        # Описание
        info = self.browser.find_elements_by_xpath('//div[@class = "ds-overview-section"]')[0].text

        # Местоположение
        adress = self.browser.find_element_by_css_selector('.ds-address-container').text

        item = ItemLoader(Zillow(), response)

        item.add_value('title',  title)
        item.add_value('info',   info)
        item.add_value('adress', adress)
        item.add_value('photos', images)
        item.add_value('params', params)

        yield item.load_item()

        print(2)

    def __del__(self):
        self.browser.close()