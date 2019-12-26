"""
Test set for the MANGA Plus scrapper.
"""
from unittest import TestCase

from scrappers.manga_plus import MangooseDatabase

__author__ = 'Ignacio Slater Muñoz'
__project__ = "Mangoose"
__email__ = "islaterm@gmail.com"
__version__ = "1.1.1.3"

# Titles
BORUTO_TITLE = "Boruto: Naruto Next Generations"
ONE_PIECE_TITLE = "One Piece"
DRAGON_BALL_SUPER_TITLE = "Dragon Ball Super"
# Links
ONE_PIECE_LINK = "https://mangaplus.shueisha.co.jp/titles/100020"
BORUTO_LINK = "https://mangaplus.shueisha.co.jp/titles/100006"
DRAGON_BALL_SUPER_LINK = "https://mangaplus.shueisha.co.jp/titles/200025"


class TestMangooseDatabase(TestCase):
    _test_database: MangooseDatabase

    def setUp(self) -> None:
        """
        Initializes the test database.
        """
        self._test_database = MangooseDatabase()

    def test_constructor(self):
        assert self._test_database.is_empty()

    def test_database_operations(self):
        assert self._test_database.is_empty()
        self._populate_db()
        self._test_add()
        self._test_remove()

    def _populate_db(self):
        self._test_database \
            .add_series(ONE_PIECE_TITLE, ONE_PIECE_LINK) \
            .add_series(BORUTO_TITLE, BORUTO_LINK) \
            .add_series(DRAGON_BALL_SUPER_TITLE, DRAGON_BALL_SUPER_LINK)

    def _test_add(self):
        assert self._test_database.size == 3, \
            f"Expected: 3, Actual: {self._test_database.size}"
        assert self._test_database.contains(ONE_PIECE_TITLE)
        assert self._test_database.get_series_link(ONE_PIECE_TITLE) == ONE_PIECE_LINK
        assert self._test_database.get_series_link(BORUTO_TITLE) == BORUTO_LINK
        assert self._test_database.get_series_link(
            DRAGON_BALL_SUPER_TITLE) == DRAGON_BALL_SUPER_LINK

    def _test_remove(self):
        self._test_database.remove(ONE_PIECE_TITLE)
        assert self._test_database.size == 2
        assert not self._test_database.contains(ONE_PIECE_TITLE)
        self._test_database.remove(ONE_PIECE_TITLE)
        assert self._test_database.size == 2
        self._test_database.remove(BORUTO_TITLE)
        self._test_database.remove(DRAGON_BALL_SUPER_TITLE)
        assert self._test_database.is_empty()
