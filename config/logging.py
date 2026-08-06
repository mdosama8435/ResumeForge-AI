import sys
from loguru import logger
from config.settings import settings

def setup_logging():
    logger.remove()
    logger.add(sys.stdout, level=settings.LOG_LEVEL)
    logger.add("app.log", rotation="10 MB", level=settings.LOG_LEVEL)
