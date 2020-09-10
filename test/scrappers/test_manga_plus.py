"""
"Mangoose" (c) by Ignacio Slater M.
"Mangoose" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""

from typing import Dict

import pytest

from scrappers.manga_plus import MangooseDatabase

@pytest.fixture
def titles() -> Dict[str, str]:
    """ Example titles used for tests.  """
    return { "Boruto: Naruto Next Generations": "https://mangaplus.shueisha.co.jp/titles/100006",
             "One Piece": "https://mangaplus.shueisha.co.jp/titles/100020",
             "Dragon Ball Super": "https://mangaplus.shueisha.co.jp/titles/200025" }


@pytest.fixture
def database() -> MangooseDatabase:
    """ Database used for tests.    """
    return MangooseDatabase()


def test_constructor(database: MangooseDatabase) -> None:
    assert database.is_empty()


def test_database_operations(database: MangooseDatabase, titles: Dict[str, str]):
    assert database.is_empty()
    populate_db(database, titles)
    expected_len = 3
    assert len(database) == expected_len
    for title, link in titles.items():
        assert title in database
        assert database[title] == link
        del database[title]
        assert title not in database
        expected_len -= 1
        assert len(database) == expected_len


def populate_db(database: MangooseDatabase, titles: Dict[str, str]) -> None:
    for title, link in titles.items():
        database[title] = link
