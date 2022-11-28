import logging
import sys


class LoggerSetup:
    def __new__(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s %(name)s %(levelname)s %(message)s",
            stream=sys.stdout,
            encoding="UTF-8",
        )
        return logging
