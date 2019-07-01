""" Module containing all the logging functionalities of mangoose.   """
import logging
from enum import Enum
from logging import Logger
from logging.handlers import RotatingFileHandler
from typing import List


class Level(Enum):
    """ Levels of the logger.   """
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

    def __init__(self, name="mangoose", level=Level.INFO):
        self._logger = logging.getLogger(name)
        self._setup(level)
        self._logger.setLevel(level.value)
        self._logger.addHandler(self._handler)

    @property
    def name(self):
        """ Name of the logger. """
        return self._logger.name

    def _setup(self, level: Level):
        raise NotImplementedError("This method is intentionally not implemented")


class MangooseFileLogger(MangooseLogger):
    """ Mangoose's app logger that logs into a file. """

    def __init__(self, level=Level.DEBUG, log_filename="mangoose.log"):
        self._filename = log_filename
        super(MangooseFileLogger, self).__init__("mangoose_file_logger", level)

    def _setup(self, level: int):
        self._handler = RotatingFileHandler(filename=self._filename, maxBytes=50000,
                                            backupCount=1)
        self._handler.setFormatter(
            "%(asctime)s:%(levelname)s:%(module)s:%(funcName)s:%(message)s")


class MangooseConsoleLogger(MangooseLogger):
    """ Mangoose's app logger that logs into console. """

    def __init__(self, level=Level.INFO):
        super(MangooseConsoleLogger, self).__init__("mangoose_console_logger", level)

    def _setup(self, level: int):
        self._handler = logging.StreamHandler()
        self._handler.setFormatter(logging.Formatter('%(message)s'))


class LoggerGroup:
    """ A class containing multiple loggers """
    _loggers: List[MangooseLogger]

    def __init__(self):
        self._logger_names = set()
        self._loggers = []

    def new_console_logger(self, level: Level = Level.INFO):
        """ Adds a new console logger to the group  """
        self._add_logger(MangooseConsoleLogger(level))

    def new_file_logger(self, level: Level = Level.INFO, filename: str = "mangoose.log"):
        """ Adds a new file logger to the group """
        self._add_logger(MangooseFileLogger(level, filename))

    def _add_logger(self, logger: MangooseLogger):
        """ Adds a new logger to the group """
        if logger.name not in self._logger_names:
            self._loggers.append(logger)
            self._logger_names.add(logger.name)

    def info(self, message: str):
        raise NotImplementedError("Info method not yet implemented")

    def error(self, message: str):
        raise NotImplementedError("Error method not yet implemented")
