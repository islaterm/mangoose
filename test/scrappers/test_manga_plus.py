"""
Test set for the MANGA Plus scrapper.
"""

__author__ = 'Ignacio Slater Muñoz'
__project__ = "Mangoose"
__email__ = "islaterm@gmail.com"
__version__ = "1.1.1.4"

# Titles
import unittest
from typing import Dict

import pytest


@pytest.fixture(scope="module")
def title_key() -> str:
    """
    Returns:    the key that represents the title of a series.
    """
    return "Title"


@pytest.fixture(scope="module")
def test_data() -> Dict[str, str]:
    # TODO: Document and refactor.
    #       The constants can be moved to a dictionary and obtained via fixtures in a
    #       cleaner way.
    BORUTO_TITLE = "Boruto: Naruto Next Generations"
    ONE_PIECE_TITLE = "One Piece"
    DRAGON_BALL_SUPER_TITLE = "Dragon Ball Super"
    # Links
    ONE_PIECE_LINK = "https://mangaplus.shueisha.co.jp/titles/100020"
    BORUTO_LINK = "https://mangaplus.shueisha.co.jp/titles/100006"
    DRAGON_BALL_SUPER_LINK = "https://mangaplus.shueisha.co.jp/titles/200025"


@pytest.fixture(scope="module")
def boruto_data() -> Dict[str, str]:
    return {}


if __name__ == '__main__':
    unittest.main()
