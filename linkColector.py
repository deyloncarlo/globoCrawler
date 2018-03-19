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
            v_file = open('links/linksCrawled.txt', 'r')
            for v_line in v_file:
                v_linksColleted.append(v_line);
            
            v_file.close()
            return v_linksColleted


        v_links = []
        v_linksColleted = getLinksCrawled()
        print("\nLendo arquivo de links...\n")
        v_file = open('links/links.txt', 'r')
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
            
            v_title = response.xpath('//h1[@class="content-head__title"]/text()').extract_first()
            v_title = toString(v_title)
            print('Titulo: ', v_title)

            v_author = response.xpath('//p[@class="content-publication-data__from"]/text()').extract_first()
            print('Valor preenchido Autor:',  v_author)
            v_author = toString(v_author)
            print('Autor: ', v_author)
            
            v_datePublished = response.xpath('//time[@itemprop="datePublished"]/text()').extract_first()
            v_datePublished = toString(v_datePublished)
            print('Data: ', v_datePublished)
            
            v_content = response.xpath('//p[contains(@class,"content-text__container")]/text()').extract()
            
            v_contentString = []
            for v_part in v_content:
                v_part = toString(v_part)
                v_contentString.append(v_part)

            print('Conteudo: ', v_contentString)
            createFileWithContent(v_title, v_author, v_datePublished, v_contentString)
            #for v_div in response.css('div.feed-text-wrapper'):
            #    v_link = v_div.css('a').xpath('@href').extract_first()
            #    v_link = v_link.encode('ascii', 'ignore')
            #    self.linkList.append(str(v_link))
            #escreverLinks()
            print('Crawler Finish')
        
        def createFileWithContent(p_title, p_author, p_date, *p_content):
            if(os.path.exists('content/' + p_author + '/') == False):
                os.mkdir('content/' + p_author + '/')   

            v_file = open('content/' + p_author + '/' + p_title + '.txt', 'w')
            v_file.write(p_title + '\n\n');
            v_file.write(p_author + '\n\n');
            v_file.write(p_date + '\n\n');
            v_file.writelines(*p_content);

            v_file.close();    

        def toString(v_content):
            v_content = v_content.encode('ascii', 'ignore')
            return str(v_content)

        schedule.every(10).seconds.do(contentCrawler, self, response)
        while True:
            schedule.run_pending()
            time.sleep(1)
