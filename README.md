# globoCrawler
Um crawler para pegar as informações das últimas reportagens do site da g1.globo.com

Criar dois contab com os seguintes comandos:
* 7 * * * sh /home/hidey/Documentos/projetos/globoCrawler/scripts/linkCrawler.sh >> /home/hidey/Documentos/projetos/globoCrawler/scripts/linkCrawler.log 2>&1

*/30 * * * * sh /home/hidey/Documentos/projetos/globoCrawler/scripts/dataCrawler.sh >> /home/hidey/Documentos/projetos/globoCrawler/scripts/dataCrawler.log 2>&1