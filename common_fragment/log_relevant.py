from loguru import logger

logger.add("file_{time}.log")
logger.add('runtime_{time}.log', rotation='00:00')
logger.add('runtime_{time}.log', rotation='1 week')
logger.add('runtime.log', retention='10 days')
logger.add('runtime_{time}.log', rotation="500 MB")