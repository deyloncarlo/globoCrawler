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

class DataCollectorCrawler(scrapy.Spider):
    name = 'dataCollectorCrawler'
    start_urls = []

    def getLinksToCrawler():

        def getLinksCrawled():
            v_linksColleted = []
            v_file = open('links/crawled_links.txt', 'r')
            for v_line in v_file:
                v_line = v_line.replace('\n', '')
                v_linksColleted.append(v_line);
            
            v_file.close()
            print("Coletados: ", v_linksColleted)
            return v_linksColleted


        v_links = []
        v_linksColleted = getLinksCrawled()
        v_file = open('links/news_link.txt', 'r')
        for v_line in v_file:
            v_line = v_line.replace('\n', '')
            if((v_line in v_linksColleted) == False):
                v_links.append(v_line);
        v_file.close()
        #print("\nFim leitura arquivo de links...\n")
        #print("Links finais: ", v_links)
        return v_links

    start_urls = [getLinksToCrawler()[0]]
    others_urls = getLinksToCrawler();
    
    def start_requests(self):
        for url in self.start_urls:
            ''' call function to manipulate url'''
            yield Request(url, self.parse)
        

    def parse(self, response):
        def contentCrawler(self, response):
            print('Crawler Start: ', response.url)
            
            v_title = response.xpath('//h1[@class="pg-color10"]/text()').extract_first()
            v_title = toString(v_title)
            print('Titulo: ', v_title)

            v_author = response.xpath('//p[@class="pg-color10"]/text()').extract_first()
            #print('Valor preenchido Autor:',  v_author)
            v_author = toString(v_author)
            v_author = re.sub('Por ', '', v_author);
            print('Autor: ', v_author)
            
            v_datePublished = response.xpath('//span[@class="data"]/text()').extract_first()
            v_datePublished = toString(v_datePublished)
            print('Data: ', v_datePublished)
            
            v_content = response.xpath('//div[@id="texto"]//p/text()[not(ancestor::*[@class="tags"])]').extract()
            
            v_contentString = '';
            for v_part in v_content:
                v_part = toString(v_part)
                v_contentString += v_part

            print('Conteudo: ', v_contentString)
            createFileWithContent(v_title, v_author, v_datePublished, v_contentString)
            writeLinkOnLinksCrawledFile(self);
            self.others_urls.remove(self.others_urls[0]);
            print('Crawler Finish')

            #if self.others_urls:
            #    print('Próxima: ', self.others_urls[0])
            #    return scrapy.Request(url=self.others_urls[0], callback=self.parse)
        
        def createFileWithContent(p_title, p_author, p_date, p_content):
            if(os.path.exists('content') == False):
                os.mkdir('content')   

            v_file = open('content/' + p_author + '.arff', 'w')
            
            v_escreveCabecalho = False            
            if os.path.getsize('content/' + p_author + '.arff') <= 0 :
                v_escreveCabecalho = True
                print("Escreve cabecalho...")

            if v_escreveCabecalho:
                v_file.write('@relation TEXTvsAUTHOR')
                v_file.write('\n\n')
                v_file.write('@attribute title string')
                v_file.write('\n')
                v_file.write('@attribute author string')
                v_file.write('\n')
                v_file.write('@attribute date string')
                v_file.write('\n')
                v_file.write('@attribute content string')
                v_file.write('\n\n')
                v_file.write('@data')
            
            v_file.write('\n')
            v_file.write( '"' + p_title + '"' + ',' + '"' + p_author + '"' + ',' + '"' + p_date + '"' + ',' + '"' + p_content + '"');
            v_file.close();


            v_globalFile = open('content/allContent.arff', 'a')
            v_escreveCabecalho = False            
            if os.path.getsize('content/allContent.arff') <= 0 :
                v_escreveCabecalho = True
                print("Escreve cabecalho...")

            if v_escreveCabecalho:
                v_globalFile.write('@relation TEXTvsAUTHOR')
                v_globalFile.write('\n\n')
                v_globalFile.write('@attribute title string')
                v_globalFile.write('\n')
                v_globalFile.write('@attribute author string')
                v_globalFile.write('\n')
                v_globalFile.write('@attribute date string')
                v_globalFile.write('\n')
                v_globalFile.write('@attribute content string')
                v_globalFile.write('\n\n')
                v_globalFile.write('@data')
            
            v_globalFile.write('\n')
            v_globalFile.write( '"' + p_title + '"' + ',' + '"' + p_author + '"' + ',' + '"' + p_date + '"' + ',' + '"' + p_content + '"');
            v_globalFile.close();

        def writeLinkOnLinksCrawledFile(self):
            if (self.others_urls[0] in ['\n', '\r\n']) == False:
                v_file = open('links/crawled_links.txt', 'a')
                v_file.write(self.others_urls[0] + '\n')

        def toString(v_content):
            v_content = v_content.encode('utf-8', 'ignore')
            v_content = str(v_content);
            return re.sub('"',"'", v_content)

        contentCrawler(self, response);
        #schedule.every(10).seconds.do(contentCrawler, self, response)
        #while True:
        #    schedule.run_pending()
        #    time.sleep(1)

process = CrawlerProcess({
    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)',
    'DEFAULT_REQUEST_HEADERS': {
        'Accept-Language': 'pt'
    }
})

process.crawl(DataCollectorCrawler)
process.start()