# -*- coding: utf-8 -*-
import scrapy


class HhVacationsSpider(scrapy.Spider):

    name = 'hh_vacations'
    allowed_domains = ['hh.ru']
    #start_urls = ['http://hh.ru/']

    key_word = 'Программист+1с'
    start_urls = ['https://spb.hh.ru/search/vacancy?text=' + key_word + '&area=2&st=searchVacancy']

    def parse(self, response):

        pagination = response.css('div.bloko-gap a.bloko-button.HH-Pager-Controls-Next::attr(href)').extract()
        if len(pagination) > 0:
            next_link = pagination[-1]
        else:
            next_link = None

        if next_link: yield response.follow(next_link, callback=self.parse)


        print(response.url)

        vacancies_pages = response.css('div.vacancy-serp a.bloko-link.HH-LinkModifier::attr(href)').extract()

        for itm in vacancies_pages:
            yield response.follow(itm, callback=self.parse_vacancy_page)

    def parse_vacancy_page(self, response):

        # заголовок вакансии
        title = response.css('h1.header span.highlighted::text').extract()
        title = ' '.join(title)

        # название и ссылку(страница hh) на компанию разместившую вакансию
        company_link = response.css('a.vacancy-company-name::attr(href)').extract_first()
        company_name = response.css('a.vacancy-company-name span::text').extract_first()


        # Все ключевые навыки
        # Не нашел на страницах (возможно, не на всех)

        # предлагаемую ЗП
        salary = response.css('p.vacancy-salary::text').extract_first()

        # Ссылку на оф сайт компании разместившую вакансию.
        yield response.follow(company_link, callback=self.parse_company_page)

        yield {
            'title': title,
            'company_link': company_link,
            'company_name': company_name,
            'salary': salary,
        }

    def parse_company_page(self, response):

        company_url = response.css('a.company-url::attr(href)').extract_first()

        yield {
            'company_url': company_url,
            'company_link': response._url
        }
        pass
