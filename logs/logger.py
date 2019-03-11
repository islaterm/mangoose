""" Module containing all the logging functionalities of mangoose.   """
import logging
from logging import Logger


class MangooseLogger:
    """ Mangoose's app logger.  """
    _logger: Logger

    def __init__(self):
        self._logger = logging.getLogger("mangoose")
        self._setup()

    def _setup(self):
        pass
