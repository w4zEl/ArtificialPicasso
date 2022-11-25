import sys
from loguru import logger
log_format = '<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> <level>{level:<8}</level> [t={thread}] {extra} ' \
             '<cyan>{file}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - {message} '
logger.remove()
logger.add(sys.stdout, format=log_format, level='INFO')
logger.add("logs/artificialpicasso_{time}.log", format=log_format, rotation="100 MB")
