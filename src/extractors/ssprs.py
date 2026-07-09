from pathlib import Path
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup

from src.utils.logger import logger



class SSPRSParser:
    def __init__(self, url='https://ssp.rs.gov.br/indicadores-da-violencia-contra-a-mulher'):
        self.url = url
        self.base_url = "https://ssp.rs.gov.br"
        self.output_dir = Path('src/data/ssprs/raw')

    def _retrieve_html(self):
        """
        Retrieve HTML from page where links to spreadsheets are avaiable

        @returns: str | None the HTML in a string format 
        """
        try:
            with httpx.Client(timeout=10.0, follow_redirects=True) as client:
                response = client.get(self.url)
                response.raise_for_status()
                return response.text
            
        except httpx.HTTPStatusError as e:
            logger.error(f'Erro de status HTTP: {e.response.status_code} para {self.url}')
            
        except Exception as e:
            logger.error(f'Conexão falhou: {e}')
            
        return None

    def parse(self):
        """
        Parse the HTML to find a div with class 'artigo__texto'
        where the links to the files are.

        @returns: a list of dictioaries containing the year of the report
        and the link download the spreadsheet 
        """
        
        html = self._retrieve_html()

        if not html:
            return []

        soup = BeautifulSoup(html, 'html.parser')
        container = soup.find('div', class_="artigo__texto")

        if not container:
            logger.error("Não há nenhuma classe `artigo__texto` no html")
            return []

        extracted_links = []
        year = ""

        for tag in container.find_all(['strong', 'a']):

            text = tag.get_text(strip=True)

            if tag.name == 'strong' and text:
                year = text.replace(" ", "_").lower()
            
            if tag.name == 'a' and tag.get('href'):
                full_url = urljoin(self.base_url, tag.get('href').__str__())

                if ".xlsx" in full_url.lower():
                    extracted_links.append({
                        "year": year,
                        "link": full_url,
                        "filename": f"{year}_raw.xlsx"
                    })
                
        return extracted_links

    def download(self, links):
        """
        Download files and output into src/data/raw folder

        @param links: list[dict[str, str]] a list of dictionaries that contains links to download files.
        """

        with httpx.Client(timeout=15.0, follow_redirects=True) as client:
            for item in links:
                target = self.output_dir / item["filename"]
                logger.warning(f"Baixando {item['link']} e colocando em {target}")

                try:
                    res = client.get(item['link'])
                    res.raise_for_status()
                    target.write_bytes(res.content)
                except Exception as e:
                    logger.error(f"Falha ao baixar {item['link']}: {e}")
