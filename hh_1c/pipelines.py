# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient

class Hh1CPipeline(object):

    def __init__(self):
        mongo_url = 'mongodb://localhost:27017'
        client = MongoClient(mongo_url)
        hh_bd = client.hh_1C
        self.hh_collec_vac = hh_bd.vacancies
        self.hh_collec_comp = hh_bd.companies

    def process_item(self, item, spider):

        if 'company_url' in item:
            self.hh_collec_comp.insert_one(item)
        else:
            self.hh_collec_vac.insert_one(item)

        return item
