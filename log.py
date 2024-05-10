import logging
from config import LOG_FILE_NAME

log_file_name = LOG_FILE_NAME

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    filename=log_file_name,
    filemode="a",
    encoding="utf8"
)


def log_info(text):
    logging.info(text)


def log_error(text):
    logging.error(text)


def get_log_file():
    return open(log_file_name, "rb")
