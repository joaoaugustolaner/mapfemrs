import scrapy


class SsprsSpider(scrapy.Spider):
    name = 'ssprs'
    allowed_domains = ['ssp.rs.gov.br']
    start_urls = [
        'https://ssp.rs.gov.br/indicadores-da-violencia-contra-a-mulher'
    ]

    def parse(self, response):
        links = [link for link in response.xpath(
            '//div[@class="artigo__texto"]/p/a/@href'
        ).getall()]

        breakpoint()
        self.logger.warn(f'{links} accessed')

        return links
