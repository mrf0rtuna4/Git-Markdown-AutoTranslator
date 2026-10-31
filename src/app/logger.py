import logging

level = logging.INFO

logging.basicConfig(level=level, format="[%(levelname)s]: %(message)s")


class Logger:
    def log_error(self, message: str) -> None:
        logging.error(message)

    def log_info(self, message: str) -> None:
        logging.info(message)

    def log_warn(self, message: str) -> None:
        logging.warning(message)

    def log_dbg(self, message: str) -> None:
        logging.debug(message)
