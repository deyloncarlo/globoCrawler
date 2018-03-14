# -*- coding: utf-8 -*-
import scrapy
import schedule
import time
from time import gmtime, strftime
import os

class GloboSpider(scrapy.Spider):
    name = 'globoSpider'
    start_urls = ['http://g1.globo.com/ultimas-noticias.html']
    
    def __init__(self):
        self.linkList = []
        self.filePath = "/home/deylon/Documentos/links/links.txt"
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
                elif ((link + '\n' in self.linksOnFile) == False):
                    arquivo.write(str(link))
                    arquivo.write("\n")
            arquivo.close()
            print("\nFim escrita no arquivo de links...\n")
        
        schedule.every().minute.do(coletarLinks, self, response)
        while True:
            schedule.run_pending()
            time.sleep(1)
