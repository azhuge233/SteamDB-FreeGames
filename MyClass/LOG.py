import logging


logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
handler = logging.FileHandler("log.txt")
handler.setLevel(logging.NOTSET)
logger.addHandler(handler)