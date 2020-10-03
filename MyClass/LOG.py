import logging


# log format
format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
format_without_levelname = logging.Formatter('%(asctime)s - %(name)s - %(message)s')

# the root logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

# file Log
f_handler = logging.FileHandler("log.txt")
f_handler.setLevel(logging.INFO)
f_handler.setFormatter(format)

# console Log
s_handler = logging.StreamHandler()
s_handler.setLevel(logging.WARNING)
s_handler.setFormatter(format_without_levelname)

# add handler to logger
logger.addHandler(f_handler)
logger.addHandler(s_handler)
