# -*- coding: utf-8 -*-
import scrapy


class TvplSpider(scrapy.Spider):
    name = 'tvpl'
    # allowed_domains = ['tuvanphapluat.vn']
    # start_urls = ['http://tuvanphapluat.vn/']

    def start_requests(self):
    	url = 'https://tuvanphapluat.vn/tu-van-luat-doanh-nghiep/thay-doi-giay-phep-kinh-doanh-lu-hanh-quoc-te-khi-doi-ten-doanh-nghiep.aspx'
    	yield scrapy.Request(url, self.parse)

    def parse(self, response):
    	#blockQuestion = 
    	#blockAnswer = 
    	detailQuestion = response.xpath('//h1[@class="title entry-title"]/a/text()').extract()
    	answerQuestion = response.xpath('//div[@class="article-content background_block entry-content"]/p/span/text()').extract()
    	record = {'detailQuestion': detailQuestion, 'answerQuestion': answerQuestion}
        print record
        for i in record:
        	for j in record[i]:
        		print j
        #pass
