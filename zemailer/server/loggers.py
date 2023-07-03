import logging
from logging.handlers import RotatingFileHandler


class BaseLogger:
    def __init__(self):
        file_handler = RotatingFileHandler(
            'app.log',
            maxBytes=1024*1024,
            backupCount=10
        )
        file_handler.setLevel(logging.INFO)
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        self.handler = file_handler


base_logger = BaseLogger()
