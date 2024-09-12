# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import MapCompose, TakeFirst

def cleaner_photo(values):
    if values[:2] == '//':
        return f'http:{values}'
    return values

def cleaner_params(item):
    # '<li class="item-params-list-item"> <span class="item-params-label">Год выпуска: </span>2010 </li>'
    result = item.split('">')[-1].split(':')
    key = result[0]
    value = result[-1].split('</span>')[-1].split('</')[0][:-1]
    return {key: value}

def cleaner_addparams(item):

    result = {}
    for itm in item['result']['insights']:
        add_itm = {itm['text'].replace('\xa0', ' '):itm['status']}
        result.update(add_itm)

    return result
    #return item

def dict_params(items):
    result = {}
    for itm in items:
        result.update(itm)
    return result

def dict_addparams(items):
    result = {}
    for itm in items:
        result.update(itm)
    return result

class Hh1CItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class AvitoCar(scrapy.Item):
    title = scrapy.Field(output_processor=TakeFirst())
    price = scrapy.Field(output_processor=TakeFirst())
    params = scrapy.Field(input_processor=MapCompose(cleaner_params), output_processor=dict_params)
    #params = scrapy.Field()
    photos = scrapy.Field(input_processor=MapCompose(cleaner_photo))
    add_params = scrapy.Field(input_processor=MapCompose(cleaner_addparams), output_processor=dict_addparams)


class Zillow(scrapy.Item):
    title = scrapy.Field()
    info = scrapy.Field()
    params = scrapy.Field()
    photos = scrapy.Field()
    adress = scrapy.Field()