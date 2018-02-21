# -*- coding: utf-8 -*-
import scrapy
from dataLaw.items import DatalawItem

class GetdataSpider(scrapy.Spider):
    name = 'getData'
    global countQA
    countQA = 0
    #allowed_domains = ['i-law.vn']
    #start_urls = ['http://i-law.vn/']

    def start_requests(self):
        urlRelative = 'https://i-law.vn/thu-vien-cau-hoi?category_id=13&keyword=&page='
        count = 0
        for page in range(0, 21):
            count = count + 1
            url = urlRelative + str(page)
            print "page ", count
            yield scrapy.Request(url, self.parse)

    def parse(self, response):
    	allUrl = response.xpath('//h3[@class="title-buyLand"]/a/@href').extract()
        print "size Url = ", len(allUrl)
        cc = 0
        for url in allUrl:
        	cc += 1
        	print "question number ", cc
        	#allUrl += ("https://i-law.vn" + url + "\n").encode('utf-8')
        	urlPage2 = ("https://i-law.vn" + url).encode('utf-8')
        	yield scrapy.Request(urlPage2, self.parseNextPage)

    def parseNextPage(self, response):
        global countQA
        countQA += 1
    	#detailQuestion = response.xpath('//p[@class=" -size text-lawyer"]/text()').extract()
        #detailQuestion = response.xpath('//div[@class = "box-detail-question"]/p/text()')
        blockQuestion = response.xpath('//div[@class = "box-detail-question"]/p/text()').extract()
        blockAnswer = response.xpath('//div[@class="description description-width description-width-responsive pull-right"]')	
        #blockAnswer = response.xpath('//div[@class="description description-width description-width-responsive pull-right"]/p/text()').extract()
        detailQuestion = []
        answerQuestion = []
        #print blockAnswer.extract()
        for i in range(1, len(blockQuestion)):
            detailQuestion.append(blockQuestion[i])

        #print "len ", len(blockAnswer)
        
        for block in blockAnswer:
        	answer = block.xpath('./p/text()').extract()
        	#answerQuestion.append(answer)
        	#print "answer ", answer
        	#print type(answer)
        	for i in range(max(0, len(answer) - 2) ):
         		answerQuestion.append(answer[i])

        if (len(answerQuestion) == 0):
         	answerQuestion.append('No answer for this question')
        
        #print "Question Number: ", countQA
        #print "url: ", response.url
        #print len(detailQuestion), len(answerQuestion)
        # print "Detal: ", detailQuestion 
        # print "Answer: ", answerQuestion
        item = DatalawItem()
        item['detailQuestion'] = detailQuestion
        item['answerQuestion'] = answerQuestion
        # # print "TYPE ", type(item['detailQuestion'])
        record = {'detailQuestion': detailQuestion, 'answerQuestion': answerQuestion}
        #print record
        # global count
        # count = 0
        # for i in record:
        #     global count 
        #     #count += 1
        #     #print "TTTT ", count 
        #     for j in record[i]:
        #         print j
               
        yield item
        #yield (u'record).encode('utf-8')
        #yield record
        #print type(answerQuestion)
        # print type(detailQuestion)
        # #yield record   


