import logging
from config import LOGGING_CONFIG

def setup_logger():
    logging.basicConfig(
        level=getattr(logging, LOGGING_CONFIG['LOG_LEVEL']),
        format=LOGGING_CONFIG['LOG_FORMAT'],
        handlers=[
            logging.FileHandler(LOGGING_CONFIG['LOG_FILE']),
            logging.StreamHandler()
        ]
    )
    return logging.getLogger(__name__)

logger = setup_logger() 