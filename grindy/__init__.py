import logging
from grindy import settings

FORMAT = '%(levelname)s:%(message)s'
logging.basicConfig(level=settings.log_level, format=FORMAT)