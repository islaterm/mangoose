"""
Scraper for MANGA Plus series.
"""
from typing import Dict

import yaml


class MangooseDatabase:
    """
    This class represents the manga database of the downloaded series and chapters.
    """
    __series: Dict[str, str]

    def __init__(self):
        self.__series = { }

    def __len__(self) -> int:
        """ Returns the size of the database. """
        return len(self.__series)

    def __contains__(self, title) -> bool:
        """ Checks if the title is in the database. """
        MangooseDatabase.__check_title_type(title)
        return title in self.__series.keys()

    def __setitem__(self, title, link) -> None:
        """ Adds an item to the database. """
        MangooseDatabase.__check_title_type(title)
        MangooseDatabase.__check_link_type(link)
        self.__series[title] = link

    def __getitem__(self, title) -> str:
        """ Adds an item to the database. """
        MangooseDatabase.__check_title_type(title)
        return self.__series[title]

    def __delitem__(self, title: str) -> None:
        """
        Removes an item from the database.
        """
        del self.__series[title]

    def is_empty(self) -> bool:
        """
        :return True if the database is empty, false otherwise.
        """
        return self.__len__() == 0

    @staticmethod
    def __check_title_type(title) -> None:
        if not type(title) is str:
            raise TypeError("Database keys should be strings")

    @staticmethod
    def __check_link_type(link):
        if not type(link) is str:
            raise TypeError("Database links should be strings")


class MangaPlusScrapper:
    """
    This class contains the functionality to scrape, parse and download manga chapters
    from MANGA Plus.
    """
    _database: MangooseDatabase

    def __init__(self, database_path: str):
        with open(database_path, "r+") as db_file:
            self._database = yaml.load(db_file, Loader=yaml.FullLoader)
