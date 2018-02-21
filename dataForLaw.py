# -*- coding: utf-8 -*-
import scrapy


class DataforlawSpider(scrapy.Spider):
    name = 'dataForLaw'
    allowed_domains = ['i-law.vn']
    start_urls = ['http://i-law.vn/']

    def parse(self, response):
        pass
