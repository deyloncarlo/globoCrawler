# -*- coding: utf-8 -*-
import scrapy
import schedule
import time
from time import gmtime, strftime
from scrapy.selector import Selector
import os
import re
from scrapy.http.request import Request
from scrapy.crawler import CrawlerProcess

class CarlosMeloCrawler(scrapy.Spider):
    name = 'carlosMeloCrawler'
    start_urls = ['http://carlosmelo.blogosfera.uol.com.br/']
    
    def __init__(self):
        self.linkList = []
        self.filePath = "links/news_link.txt"
        self.linksOnFile = []
        print("\nLendo arquivo de links...\n")
        v_arquivo = open(self.filePath, 'r')
        for v_linha in v_arquivo:
           self.linksOnFile.append(v_linha)
       
        v_arquivo.close()
        print("\nFim leitura arquivo de links...\n")
            
    def parse(self, response):
        def coletarLinks(self, response):
            self.linkList = []
            for v_article in response.css('article.post.news'):
                v_h1 = v_article.css('h1')
                v_link = v_h1.css('a').xpath('@href').extract_first()
                v_link = v_link.encode('ascii', 'ignore')
                self.linkList.append(str(v_link))
            escreverLinks()
                    
        def escreverLinks():
            print("\nEscrevendo no arquivo de links...\n")
            arquivo = open(self.filePath, 'a')
        
            for link in self.linkList:
                if(link + '\n' in self.linksOnFile):
                    print('Link já coletado: ', link)
                elif ((link) + '\n' in self.linksOnFile) == False:
                    arquivo.write(str(link))
                    arquivo.write("\n")
            arquivo.close()
            print("\nFim escrita no arquivo de links...\n")
        
        coletarLinks(self, response)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(CarlosMeloCrawler)
process.start()