import logging
from config.settings import settings
import sys

def setup_logging(): 
    logging.basicConfig(
        level=logging.INFO,
        format=settings.format_logging,
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )