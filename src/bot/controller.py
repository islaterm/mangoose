"""
This module contains the controller that handles all the bot's input
"""

__author__ = "Ignacio Slater Muñoz"
__version__ = "2.0.2"

from logs.logger import LoggerGroup, NullLogger


class MangooseBot:
    """
    Main interface of Mangoose
    """
    _token: str

    def __init__(self, test: bool = False):
        """
        Setup the parameters and runs a new bot with the token retrieved from the
        config.json file

        :param test:
            flag that indicates if the bot is running on test mode
        """
        if test:
            self._loggers = NullLogger()
        else:
            self._loggers = LoggerGroup()
            self._loggers.new_console_logger()
            self._loggers.new_file_logger()
