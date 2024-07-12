import logging

logging.basicConfig(level=logging.INFO, format='%(levelname)s - %(message)s')

def log_error(message):
    logging.error(message)

def log_info(message):
    logging.info(message)
