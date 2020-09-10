"""
"Mangoose" (c) by Ignacio Slater M.
"Mangoose" is licensed under a
Creative Commons Attribution 4.0 International License.
You should have received a copy of the license along with this
work. If not, see <http://creativecommons.org/licenses/by/4.0/>.
"""
import unittest
from typing import Dict

import pytest

from scrappers.manga_plus import MangooseDatabase


def test_constructor(database: MangooseDatabase):
    assert database.is_empty()


def test_database_operations(database: MangooseDatabase, mangas: Dict[str, str]) -> None:
    assert database.is_empty()
    with pytest.raises(TypeError):
        assert 1 in database
    with pytest.raises(TypeError):
        database["wrong"] = 1
    check_add(database, mangas)
    check_remove(database, mangas)


def check_add(database: MangooseDatabase, mangas: Dict[str, str]):
    assert len(database) == 0
    for title, link in mangas.items():
        database[title] = link
        assert title in database
        assert database[title] == link


def check_remove(database: MangooseDatabase, mangas: Dict[str, str]):
    expected_size = len(mangas)
    assert len(database) == expected_size
    for title, _ in mangas.items():
        del database[title]
        expected_size -= 1
        assert len(database) == expected_size
        assert not title in database
    assert database.is_empty()


@pytest.fixture
def database() -> MangooseDatabase:
    return MangooseDatabase()


@pytest.fixture()
def mangas() -> Dict[str, str]:
    return { "Boruto: Naruto Next Generations": "https://mangaplus.shueisha.co.jp/titles/100020",
             "One Piece": "https://mangaplus.shueisha.co.jp/titles/100006",
             "Dragon Ball Super": "https://mangaplus.shueisha.co.jp/titles/200025" }


if __name__ == '__main__':
    unittest.main()
