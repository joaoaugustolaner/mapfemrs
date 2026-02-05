import scrapy


class SsprsSpider(scrapy.Spider):
    name = "ssprs"
    allowed_domains = ["ssp.rs.gov.br"]
    start_urls = ["https://ssp.rs.gov.br/indicadores-da-violencia-contra-a-mulher"]

    def parse(self, response):
        for link in response.xpath('//div[@class="artigo__texto"]/p/a/@href').getall():
            self.logger.warn(f"{link} accessed")
            pass
