""" Module containing all the logging functionalities of mangoose.   """
import logging
from logging import Logger
from logging.handlers import RotatingFileHandler
from typing import List

DEBUG = logging.DEBUG
INFO = logging.INFO
CRITICAL = logging.CRITICAL
ERROR = logging.ERROR
WARNING = logging.WARNING


class MangooseLogger:
    """ Mangoose's app logger.  """
    _handler: logging.StreamHandler
    _level: int
    _logger: Logger

    def __init__(self, name="mangoose", level=INFO):
        self._logger = logging.getLogger(name)
        self._setup(level)
        self._logger.setLevel(level)
        self._logger.addHandler(self._handler)

    def _setup(self, level: int):
        raise NotImplementedError("This method is intentionally not implemented")


class MangooseFileLogger(MangooseLogger):
    """ Mangoose's app logger that logs into a file. """

    def __init__(self, level=DEBUG):
        super(MangooseFileLogger, self).__init__("mangoose_file_logger", level)

    def _setup(self, level: int):
        self._handler = RotatingFileHandler(filename="mangoose.log", maxBytes=50000,
                                            backupCount=1)
        self._handler.setFormatter(
            "%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s")


class MangooseConsoleLogger(MangooseLogger):
    """ Mangoose's app logger that logs into console. """

    def __init__(self, level=INFO):
        super(MangooseConsoleLogger, self).__init__("mangoose_console_logger", level)

    def _setup(self, level: int):
        self._handler = logging.StreamHandler()
        self._handler.setFormatter(logging.Formatter('%(message)s'))


class LoggerGroup:
    """ A class containing multiple loggers """
    _loggers: List[MangooseLogger]

    def __init__(self):
        self._loggers = []

    def add_logger(self, logger: MangooseLogger):
        """ Adds a new logger to the group """
        self._loggers.append(logger)

    def info(self, message: str):
        raise NotImplementedError("Info method not yet implemented")

    def error(self, message: str):
        raise NotImplementedError("Error method not yet implemented")
