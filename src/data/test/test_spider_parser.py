import os

from scrapy.http import HtmlResponse, Request

from src.data.data.spiders.ssprs import SsprsSpider


def test_should_return_a_list_containing_sample_of_links_from_html():

    current_dir = os.path.dirname(__file__)

    fixture_path = os.path.join(current_dir, 'fixtures', 'sample.html')
    with open(
            fixture_path,
            'r',
            encoding='utf-8') as file:
        html_test = file.read()

        response = HtmlResponse(
            url='https://ssprs.rs.gov.br',
            body=html_test,
            encoding='utf-8',
            request=Request(url='https://example.com'),
        )

        spider = SsprsSpider()
        result = list(spider.parse(response))

        assert len(result) > 0
        assert result[0]['file_url'].__contains__('upload/arquivos')
