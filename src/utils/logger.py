import logging
import sys

LOGGING_FORMAT = '%(asctime)s - [%(levelname)s] - %(message)s'
DATE_FORMAT = '%Y - %m - %d'

logging.basicConfig(
    level=logging.DEBUG,
    format = LOGGING_FORMAT,
    datefmt= DATE_FORMAT,
    handlers = [logging.StreamHandler(sys.stderr)],
)

logger = logging.getLogger('logger')
