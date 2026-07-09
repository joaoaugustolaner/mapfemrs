from datetime import date
from pathlib import Path

from pysus.online_data.SINAN import SINAN

from src.utils.logger import logger


class Sinan():

    START_YEAR = 2012
    DISEASE_CODE = 'VIOL'
    
    def __init__(self):
        self.output_dir = Path('src/data/sinan/')

    def donwload(self):
        sinan = SINAN().load()
        logger.warning('Starting download of SINAN files...')

        for year in range(self.START_YEAR, date.today().year):
            sinan.download(sinan.get_files('VIOL', year, local_dir=self.output_dir))
            logger.info(f"[DOWNLOAD] - File {year} downloaded")
