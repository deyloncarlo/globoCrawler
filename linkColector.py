# -*- coding: utf-8 -*-
import scrapy
import schedule
import time
from time import gmtime, strftime
from scrapy.selector import Selector
import os

class LinkCrawler(scrapy.Spider):
    name = 'linkCrawler'

    def getLinksToCrawler():

        def getLinksCrawled():
            v_linksColleted = []
            v_file = open('/home/deylon/Documentos/links/linksCrawled.txt', 'r')
            for v_line in v_file:
                v_linksColleted.append(v_line);
            
            v_file.close()
            return v_linksColleted


        v_links = []
        v_linksColleted = getLinksCrawled()
        print("\nLendo arquivo de links...\n")
        v_file = open('/home/deylon/Documentos/links/links.txt', 'r')
        for v_line in v_file:
            if((v_line in v_linksColleted) == False):
                v_line = v_line.replace('\n', '')
                v_links.append(v_line);

        v_file.close()
        print("\nFim leitura arquivo de links...\n")
        print("Links finais: ", v_links)
        return v_links

    start_urls = getLinksToCrawler()
    
    def parse(self, response):
        def contentCrawler(self, response):
            print('Crawler Start')
            v_titulo = response.xpath('//h1[@class="content-head__title"]/text()').extract_first()
            print('H1?: ', h1)

            #for v_div in response.css('div.feed-text-wrapper'):
            #    v_link = v_div.css('a').xpath('@href').extract_first()
            #    v_link = v_link.encode('ascii', 'ignore')
            #    self.linkList.append(str(v_link))
            #escreverLinks()
            print('Crawler Finish')
                    
        schedule.every(10).seconds.do(contentCrawler, self, response)
        while True:
            schedule.run_pending()
            time.sleep(1)
