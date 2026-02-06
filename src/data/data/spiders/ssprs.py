import scrapy


class SsprsSpider(scrapy.Spider):

    base_url = 'https://ssp.rs.gov.br/'
    name = 'ssprs'
    allowed_domains = ['ssp.rs.gov.br']
    start_urls = [
        'https://ssp.rs.gov.br/indicadores-da-violencia-contra-a-mulher'
    ]

    def parse(self, response):
        links = response.xpath("//div[contains(@class, 'artigo__texto')]//a[contains(@href, '.xlsx')]/@href").getall()
        
        
        for link in links:
            if(link).__contains__('admin'):
                
            yield {
                'file_url':link
            }
        
