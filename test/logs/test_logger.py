""" Tests for the mangoose logger module.   """
from unittest import TestCase

from logs.logger import MangooseLogger

__author__ = "Ignacio Slater Muñoz"
__version__ = "2.0b1"


class TestMangooseLogger(TestCase):
    """ Mangoose logger tests.  """
    _logger: MangooseLogger

    def setUp(self):
        """ Tests initial config.   """
        self._logger = MangooseLogger()
