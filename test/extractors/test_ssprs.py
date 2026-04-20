from pathlib import Path

import httpx
import pytest
from bs4 import BeautifulSoup

from src.extractors.ssprs import SSPRSParser


@pytest.fixture
def html_template():
    return """
    <div class="artigo__texto">
        <p><strong>2026</strong></p>
        <p><a href="/test_2026.xlsx">Link 2026</a></p>
        <p><strong>2025</strong></p>
        <p><a href="/test_2025.xlsx">Link 2025</a></p>
    </div>
    """


@pytest.fixture
def parser(tmp_path):
    """
    Initializes parser with a temporary directory for output
    to avoid writing to your actual src/data/raw during tests.
    """
    p = SSPRSParser()
    p.output_dir = tmp_path
    return p


def test_retrieve_html_success(parser, mocker, html_template):

    mock_response = mocker.Mock()
    mock_response.text = html_template
    mock_response.status_code = 200

    mock_client = mocker.patch("httpx.Client.get", return_value=mock_response)

    result = parser._retrieve_html()
    assert result == html_template
    assert mock_client.called


def test_retrieve_html_http_error(parser, mocker):

    mock_response = mocker.Mock()
    mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
        "404 Not Found", request=mocker.Mock(), response=mock_response
    )
    mock_response.status_code = 404

    mocker.patch("httpx.Client.get", return_value=mock_response)

    result = parser._retrieve_html()
    assert result is None


def test_parse_success(parser, mocker, html_template):

    mocker.patch.object(parser, "_retrieve_html", return_value=html_template)

    links = parser.parse()

    assert len(links) == 2
    assert links[0]["year"] == "2026"
    assert links[0]["filename"] == "2026_raw.xlsx"
    assert "https://ssp.rs.gov.br/test_2026.xlsx" in links[0]["link"]


def test_parse_no_container(parser, mocker):
    mocker.patch.object(
        parser, "_retrieve_html", return_value="<html><body>Empty</body></html>"
    )
    links = parser.parse()
    assert links == []


def test_download_success(parser, mocker):

    test_links = [
        {
            "year": "2026",
            "link": "https://ssp.rs.gov.br/file.xlsx",
            "filename": "2026_raw.xlsx",
            "url": "https://ssp.rs.gov.br/file.xlsx",
        }
    ]

    mock_response = mocker.Mock()
    mock_response.content = b"fake_excel_content"
    mock_response.status_code = 200

    mocker.patch("httpx.Client.get", return_value=mock_response)

    parser.download(test_links)

    expected_file = parser.output_dir / "2026_raw.xlsx"
    assert expected_file.exists()
    assert expected_file.read_bytes() == b"fake_excel_content"

def test_download_failure_continues(parser, mocker):

    test_links = [
        {"filename": "fail.xlsx", "link": "http://fail.com"},
        {"filename": "success.xlsx", "link": "http://success.com"}
    ]
    
    def side_effect(url, **kwargs):
        if "fail" in url:
            raise Exception("Network down")
        mock = mocker.Mock()
        mock.content = b"success"
        return mock

    mocker.patch("httpx.Client.get", side_effect=side_effect)
    
    parser.download(test_links)
    
    assert not (parser.output_dir / "fail.xlsx").exists()
    assert (parser.output_dir / "success.xlsx").exists()
