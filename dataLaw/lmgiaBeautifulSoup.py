# -*- coding: utf-8 -*-
import urllib2
import urllib
from bs4 import BeautifulSoup
import codecs
import re
import sys
import json
reload(sys)
sys.setdefaultencoding('utf-8')
data = {}
class item:
	def __init__(self, question, answer, url):
		self.question = question
		self.answer = answer
		self.url = url

def getAllLink():
	links  = []
	prefixUrl = "https://luatminhgia.com.vn/hoi-dap-doanh-nghiep.aspx?page="
	coreUrl = "https://luatminhgia.com.vn"

	for i in range(1, 78):
		urlDetail = "https://luatminhgia.com.vn/hoi-dap-doanh-nghiep.aspx?page=%s"%(urllib.quote(str(i)))
		page = urllib2.urlopen(urlDetail)
		soup = BeautifulSoup(page, 'html.parser')
		texts = soup.findAll('div', attrs = {'class': "item clearfix"})
		for i in texts:
			textLower = i.find('a', attrs = {'class': 'title'})
			#fullLink = coreUrl + textLower['href'].encode('utf-8') 
			fullLink = "https://luatminhgia.com.vn%s"%(urllib.quote( textLower['href'].encode('utf-8') ))
			
			links.append(fullLink)
	return links
def getQA(url):
	print "Url:", url
	#f = codecs.open("lmgiaData.", "a", encoding="utf-8")
	page = urllib2.urlopen(url)
	soup = BeautifulSoup(page, 'html.parser')
	texts = soup.find('div', attrs = {'class': 'news_view content clearfix'})
	textLower  = texts.findAll(['div'])
	#f.write(textLower[2].text)
	#f.write(textLower[4].text)
	#print textLower[2].text
	lenAnswer = 0
	pos = -1
	for i in range(3, 6):
		#print "Number: ", i
		if (lenAnswer < len(textLower[i].text)):
			lenAnswer = len(textLower[i].text)
			pos = i
		
	
	ret = item(textLower[2].text, textLower[pos].text, url)
	#print textLower[pos].text
	#print len(textLower[2].text), " ", len(textLower[4].text), " ", len(textLower[5].text)
	#print type(textLower[2].text), type(textLower[4].text)
	#global data 
	data['item'].append(ret.__dict__)

	#json.dump(ret.__dict__, f, ensure_ascii=False)

	#print ret.__dict__['question']
	#f.write(textLower[2].text.encode('utf8'))
	#yield ret
def testPerLink():
	url = "https://luatminhgia.com.vn/hoi-dap-doanh-nghiep/cong-ty-muo%CC%81n-thu%CC%A3c-hie%CC%A3n-du%CC%A3-a%CC%81n-co%CC%81-pha%CC%89i-xin-phe%CC%81p-.aspx"
	getQA(url)
def startCrawler():

	allLinks = getAllLink()
	print len(allLinks)
	data['item'] = [] 
	f = codecs.open("lmgiaData.json", "a", encoding="utf-8")
	for i in range(0, len(allLinks)):
		#f.write(i + "\n")
		# if (i == 15):
		# 	continue
		print "Link number: ", i
		getQA(allLinks[i])
	#json.dump(data, f)
	
	json.dump(data, f, ensure_ascii=False)
	#print textLower 
	 	#print len(text2.text)
	#getQA("https://luatminhgia.com.vn/luat-su-doanh-nghiep/tong-dai-luat-su-tu-van-phap-luat-doanh-nghiep-19006169.aspx")
#testPerLink()
startCrawler()

	#print soup.pretify
#getText()