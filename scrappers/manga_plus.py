"""
Scraper for MANGA Plus series.
"""
from typing import Dict

import yaml

__author__ = 'Ignacio Slater Muñoz'
__project__ = "Mangoose"
__email__ = "islaterm@gmail.com"
__version__ = "1.1.1.3"


class MangooseDatabase:
    """
    This class represents the manga database of the downloaded series and chapters.
    """
    _series: Dict[str, str]

    def __init__(self):
        """
        Creates an empty database.
        """
        self._series = {}

    @property
    def size(self) -> int:
        """
        :return: the number of entries in the database.
        """
        return len(self._series)

    def is_empty(self):
        """
        :return: True if the database is empty, false otherwise.
        """
        return self.size == 0

    def add_series(self, name: str, link: str) -> 'MangooseDatabase':
        """
        Adds a new series to the database with a link to the webpage containing the
        chapters.
        :return: the updated database.
        """
        self._series[name] = link
        return self

    def contains(self, param):
        pass

    def get_series_link(self, param):
        pass

    def remove(self, ONE_PIECE_TITLE):
        pass


class MangaPlusScrapper:
    """
    This class contains the functionality to scrape, parse and download manga chapters
    from MANGA Plus.
    """
    _database: MangooseDatabase

    def __init__(self, database_path: str):
        with open(database_path, "r+") as db_file:
            self._database = yaml.load(db_file, Loader=yaml.FullLoader)
