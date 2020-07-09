"""
Scraper for MANGA Plus series.
"""
from typing import Dict

import yaml

__version__ = "2.0-b.2"


class MangooseDatabase:
    """
    This class represents the manga database of the downloaded series and chapters.
    """
    _series: Dict[str, str]

    def __init__(self):
        self._series = { }

    def __len__(self) -> int:
        """ Returns the size of the database. """
        return len(self._series)

    def __contains__(self, title) -> bool:
        """ Checks if the title is in the database. """
        if not type(title) is str:
            raise TypeError("Database keys should be strings")
        return title in self._series.keys()

    def is_empty(self) -> bool:
        """
        :return True if the database is empty, false otherwise.
        """
        return self.__len__() == 0

    def add_series(self, param: str, param1: str) -> 'MangooseDatabase':
        pass

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
