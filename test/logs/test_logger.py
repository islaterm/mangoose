""" Tests for the mangoose logger module.   """
from unittest import TestCase

from logs.logger import MangooseLogger


class TestMangooseLogger(TestCase):
    """ Mangoose logger tests.  """
    _logger: MangooseLogger

    def setUp(self):
        """ Tests initial config.   """
        self._logger = MangooseLogger()
