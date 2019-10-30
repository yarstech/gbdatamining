# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from sqdatabase.database import KvartiryBase
from sqdatabase.models import KvartiraPost, Photos, Base

class Hh1CPipeline(object):

    def __init__(self):
        #mongo_url = 'mongodb://localhost:27017'
        #client = MongoClient(mongo_url)
        #hh_bd = client.hh_1C
        #self.hh_collec_vac = hh_bd.vacancies
        #self.hh_collec_comp = hh_bd.companies

        bd_url = 'sqlite:///kvartiry_base.sqlite'
        self.bd = KvartiryBase(Base, bd_url)

    def process_item(self, item, spider):
        if spider.name == "hh_vacations":
            if 'company_url' in item:
                self.hh_collec_comp.insert_one(item)
            else:
                self.hh_collec_vac.insert_one(item)

        if spider.name == "avito":

            kvartira_post = KvartiraPost(item['title'], item['kvartira_url'],
                                         item['author_url'], item['location'])

            self.bd.session.add(kvartira_post)

            for itm in item['photos']:
                photo_post = Photos(itm, kvartira_post)
                self.bd.session.add(photo_post)

            try:
                self.bd.session.commit()
            except Exception as e:
                print(e)
            pass

        return item
