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

class GloboSpider(scrapy.Spider):
    name = 'globoSpider'
    start_urls = ['http://g1.globo.com/economia/']
    
    def __init__(self):
        self.linkList = []
        self.filePath = "links/links.txt"
        self.linksOnFile = []
        print("\nLendo arquivo de links...\n")
        v_arquivo = open(self.filePath, 'r')
        for v_linha in v_arquivo:
            self.linksOnFile.append(v_linha);
        
        v_arquivo.close()
        print("\nFim leitura arquivo de links...\n")
            
    def parse(self, response):
        def coletarLinks(self, response):
            self.linkList = []
            for v_div in response.css('div.feed-text-wrapper'):
                v_link = v_div.css('a').xpath('@href').extract_first()
                v_link = v_link.encode('ascii', 'ignore')
                self.linkList.append(str(v_link))
            escreverLinks()
            
        def obterLinksExistentes():
            self.linksOnFile = []
            print("\nLendo arquivo de links...\n")
            v_arquivo = open(self.filePath, 'r')
            for v_linha in v_arquivo:
                self.linksOnFile.append(v_linha);
        
            v_arquivo.close()
            print("\nFim leitura arquivo de links...\n")
            print('Links encontrados: \n', self.linksOnFile)
        
        
        def escreverLinks():
            obterLinksExistentes()
        
            print("\nEscrevendo no arquivo de links...\n")
            arquivo = open(self.filePath, 'a')
        
            for link in self.linkList:
                if(link + '\n' in self.linksOnFile):
                    print('Link já coletado: ', link)
                elif ((link) + '\n' in self.linksOnFile) == False and ('/economia/' in link):
                    arquivo.write(str(link))
                    arquivo.write("\n")
            arquivo.close()
            print("\nFim escrita no arquivo de links...\n")
        
        coletarLinks(self, response)
        #schedule.every().day.at("20:00").do(coletarLinks, self, response)
        #while True:
        #    schedule.run_pending()
        #    time.sleep(1)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
})

process.crawl(GloboSpider)
process.start()