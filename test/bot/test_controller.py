import unittest

from bot.controller import MangooseBot

__author__ = "Ignacio Slater Muñoz"
__version__ = "1.1.1.4"


class MyTestCase(unittest.TestCase):
    _bot: MangooseBot

    # TODO: Test controller constructor (correct and missing config cases)
    def setUp(self) -> None:
        pass

    def test_something(self):
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
