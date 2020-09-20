""" "Mangoose" (c) by Ignacio Slater M.
    "Mangoose" is licensed under a
    Creative Commons Attribution 4.0 International License.

    You should have received a copy of the license along with this
    work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import logging
from logging.handlers import RotatingFileHandler


class MangooseLogger:
    """ Wrapper class to handle the bot logs. """
    __logger: logging.Logger

    def __init__(self, context: str):
        self.__logger = logging.getLogger(context)
        self.__logger.setLevel(logging.DEBUG)
        console_logger = logging.StreamHandler()
        console_logger.setLevel(logging.DEBUG)
        console_logger.setFormatter(
            logging.Formatter('%(levelname)s:%(name)s:%(message)s'))
        self.__logger.addHandler(console_logger)
        file_logger = RotatingFileHandler(filename='logs/mangoose.log', encoding="utf-8",
                                          maxBytes=50000, backupCount=2)
        file_logger.setLevel(logging.INFO)
        file_logger.setFormatter(
            logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        self.__logger.addHandler(file_logger)

    def debug(self, msg: str) -> None:
        """ Logs a message with debug level.    """
        self.__logger.debug(msg)

    def info(self, msg: str) -> None:
        """ Logs a message with info level.    """
        self.__logger.info(msg)

    def error(self, msg: str) -> None:
        """ Logs a message with error level.    """
        self.__logger.error(msg)

    def critical(self, msg: str) -> None:
        """ Logs a message with error level.    """
        self.__logger.critical(msg)
