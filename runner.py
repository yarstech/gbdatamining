from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings

from hh_1c import settings
from hh_1c.spiders.hh_vacations import HhVacationsSpider
from hh_1c.spiders.avito import AvitoSpider
from hh_1c.spiders.avito_cars import AvitoCarsSpider

from hh_1c.spiders.instagram import InstagramSpider
from config import INSAT_LOGIN, INSAT_PASS

if __name__ == '__main__':
    crawler_settings = Settings()
    crawler_settings.setmodule(settings)

    process = CrawlerProcess(settings=crawler_settings)
    #process.crawl(HhVacationsSpider)
    #process.crawl(AvitoSpider)
    #process.crawl(AvitoCarsSpider)

    users = ['putinofficial.ru', 'timatiofficial_fanpage']
    process.crawl(InstagramSpider, INSAT_LOGIN, INSAT_PASS, users)
    process.start()