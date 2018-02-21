# -*- coding: utf-8 -*-
import scrapy
import re
import codecs
def cleanHtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

class LmgiaSpider(scrapy.Spider):
    name = 'lmgia'
    # allowed_domains = ['luatminhgia.com.vn']
    # start_urls = ['http://luatminhgia.com.vn/']

    def start_requests(self):
        url = 'https://luatminhgia.com.vn/hoi-dap-doanh-nghiep/luat-su-tu-van-ve-nganh-nghe-kinh-doanh-co-dieu-kien.aspx'
    	#url = 'https://luatminhgia.com.vn/hoi-dap-doanh-nghiep/hoi-ve-dieu-kien-bo-sung-nganh-nghe-kinh-doanh-nhap-khau-xe-cu-.aspx'
    	#url = 'https://luatminhgia.com.vn/hoi-dap-doanh-nghiep/thay-doi-giam-doc-trung-tam-ngoai-ngu-tin-hoc.aspx'
    	yield scrapy.Request(url, self.parse)
    def parse(self, response):
    	#blockQuestion = 
    	#blockAnswer = 
    	#detailQuestion = response.xpath('//div[@style = "font-weight: bold; padding-bottom: 10px;"]/text()').extract()
    	#answerQuestion = response.xpath('//p[@style="text-align:justify"]/span/text()').extract()
    	blockDiv = response.xpath('//div[@class="news_view content clearfix"]')

    	blockDiv2 = blockDiv.xpath('./div[@class="article-mainRelate"]/h3/text()')
    	f = codecs.open("lmgia.txt", "w", encoding="utf-8")
        #f.write(cleanHtml(blockDiv.extract()))
        #f.write(blockDiv.extract())
        blockQues = blockDiv.xpath('./div[@style="font-weight: bold; padding-bottom: 10px;"]/text()').extract()
        #print len(blockQues)
        blockFull = blockDiv.xpath('./div').extract()
        blockTagBaiViet = blockDiv.xpath('./div[@class="tag-baiviet"]').extract()
        id = len(blockFull) - 3
        print "TagbaiViet", type(blockTagBaiViet)
        if (len(blockTagBaiViet) > 0):
            id -= 1
        out = cleanHtml(blockFull[id])
        print "TYPE OUT: ", type(out)
        # nonBreakSpace = u'\xa0'
        # out.replace(nonBreakSpace, '')
        # f.write(out)
        for i in out:
            print "TYPE I: ", type(i)
            break
        # for i in blockFull[len(blockFull) - 3]:
        #     f.write(cleanHtml(i))
        # #print "Len block full: ", len(blockFull)
        # for i in blockQues:
        #     f.write(i)

        #print type(blockQues.extract())
        #print type(blockQues)
        # for i in blockDiv:
        #     f.write(cleanHtml(i.extract()))
        #     #print type(i.extract()) 
        #print type(blockDiv.extract())
    	# for i in range(0, len(blockDiv)):
    	# 	#print "Block Number: ", i
    	# 	#print cleanHtml(blockDiv[i].extract())
    	# 	#print type(cleanHtml(blockDiv[i].extract()))
    	# 	f.write("Block number: " + str(i))
    	# 	#out  = cleanHtml(blockDiv[i].extract())
    	# 	#print type(cleanHtml(blockDiv[i].extract()))
    	# 	#out2 = out.encode('utf-8')
    	# 	#f.write(out2)
    	# 	f.write(cleanHtml(blockDiv[i].extract()))
    	
    	#print blockDiv
    	# pos = -1
    	for i in range(0, len(blockDiv)):
    	 	blockMainRelate = blockDiv[i].xpath('./div[@class="article-mainRelate"]/h3/text()').extract()
    	 	if (len(blockMainRelate) > 0):
    	 		#f.write("Block number: " + str(i))
    	# 		#print cleanHtml(blockDiv[i].extract())
    	# 		print blockMainRelate w
    			f.write(cleanHtml(blockDiv[i].extract()))
    			print "len = ", len(blockDiv[i].extract()) 
    	# 		pos = i
    	# 		break

    	# print "Position main relate: ", pos
    	# # for i in range(0, len(blockDiv)):
    	# 	print "Block number: ", i ]

    	# 	print cleanhtml(blockDiv[i) 
    	# # record = {'detailQuestion': detailQuestion, 'answerQuestion': answerQuestion}
     #   	#print record
     #    for i in record:
     #    	for j in record[i]:
     #    		print j
