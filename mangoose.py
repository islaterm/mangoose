#!/usr/bin/python
# coding=utf-8
"""
Mango eating mongoose.
"""
import argparse
import json
import os
import shutil
from typing import List

import certifi
import requests
import tqdm as tqdm
import urllib3
from bs4 import BeautifulSoup

from logs.logger import LoggerGroup

__author__ = 'Ignacio Slater Muñoz'
__project__ = "Mangoose"
__email__ = "islaterm@gmail.com"
__version__ = "0.2.004"


class MangaPage:
    _page_number: str
    _page_url: str

    def __init__(self, page_url: str, page_number: int):
        self._page_url = page_url
        self._page_number = str(page_number).zfill(3)

    def download(self, dest_path: str):
        response_image = requests.get(self._page_url, timeout=60)
        content_type = response_image.headers["Content-Type"]
        img_extension = content_type.split("/")[-1]
        file_name = f"{self._page_number}.{img_extension}"
        filepath = os.path.join(dest_path, file_name)
        with open(filepath, 'wb') as img:
            img.write(response_image.content)


def validate(title):
    title = title.replace(": ", " - ").replace(':', '-').replace('?', '_').replace('/',
                                                                                   '_')
    return title


def create_cbz(dir_path: str):
    """ Creates a .cbz file from a directory and the deletes the directory.
    :param dir_path: Path to the directory.
    """
    zip_file = shutil.make_archive(dir_path, 'zip', dir_path)
    shutil.rmtree(dir_path, ignore_errors=True)
    base, _ = os.path.splitext(zip_file)
    os.rename(zip_file, f"{base}.cbz")


def download(chapter, dest_path):
    i = 1
    manga_pages: List[MangaPage] = []
    while True:
        page_response = http.request('GET', chapter[1] + "/" + str(i))
        page_soup = BeautifulSoup(page_response.data, "html.parser")
        try:
            manga_pages.append(MangaPage(
                "https:" + page_soup.find('img', {"id": "manga-page"}).attrs['src'], i))
        except AttributeError:  # Se llegó a la última página
            break
        i += 1
    print(f"Downloading {chapter[0]}")
    for page in tqdm.tqdm(manga_pages):
        page.download(dest_path)
    create_cbz(dest_path)


def eat():
    for title in series:
        # noinspection PyTypeChecker
        eat_mango(title, series[title]["url"],
                  series[title]["downloaded_chapters"])


def eat_mango(manga_name: str, manga_url: str, skip=None):
    loggers.info(f"Looking for chapters for {manga_name}")
    if skip is None:
        skip = []
    response = http.request('GET', manga_url)
    soup = BeautifulSoup(response.data, "html.parser")
    chapters = get_chapters(soup)
    for chapter in reversed(chapters):
        chapter_title = chapter[0]
        chapter_id = chapter_title.split("-")[0].strip()
        if chapter_id in skip:
            continue
        valid_title = (
            validate(manga_name),
            validate(chapter_title),
        )
        filename = valid_title[0] + " C" + valid_title[1] + " [EN]"
        dir_path = os.path.join(downloads_folder, valid_title[0], filename)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        try:
            download(chapter, dir_path)
            # noinspection PyTypeChecker
            series[manga_name]["downloaded_chapters"].append(chapter_id)

            with open("settings.json", 'w') as json_file:
                json.dump(config, json_file, indent=2)
        except Exception:
            raise Exception          


def parse_table(table):
    entries = []
    for element in table:
        url_prefix = "https://readms.net" + "/".join(
            element.attrs['href'].split('/')[:-1])
        entries.append((element.contents[0], url_prefix))
    return entries


def get_chapters(soup_url: BeautifulSoup):
    chapters_table = soup_url.find("table", {"class": "table table-striped"})
    chapters = parse_table(chapters_table.find_all("a"))
    return chapters


def setup_parser(a_parser):
    a_parser.add_argument(
        "-d",
        "--SetDownloadsFolder",
        help="Sets the destination folder for the downloaded mangas.")
    a_parser.add_argument(
        "-l",
        "--Logging",
        help="Writes execution info to a file.",
        action="store_true",
        default=False)
    a_parser.add_argument(
        "-q",
        "--Quiet",
        help="Turns off std out printing.",
        action="store_true",
        default=False)
    group = a_parser.add_mutually_exclusive_group()
    group.add_argument(
        "-n",
        "--NewSeries",
        help=
        "Adds a new series to the download list. For this to work you need to provide a "
        "name for the series and a valid link to the manga site containing the chapters.",
        nargs=2)
    group.add_argument(
        "-a",
        "--Auto",
        help=
        "Downloads all the mangas added to the download list (skipping already downloaded "
        "chapters).",
        action="store_true")
    group.add_argument(
        "--Delete",
        help="Deletes a series from the downloads list. This can't be undone.")
    a_parser.epilog = 'An example of usage could be: mangoose.py -n \"Boku no Hero Academia\" ' \
                      '\"https://readms.net/manga/my_hero_academia\" -d \"C:\\downloads\" -l'


def set_downloads_folder(new_path):
    new_path = os.path.normpath(new_path)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
        loggers.info("Created directory " + new_path)
    config["downloads_folder"] = new_path
    with open("settings.json", 'w') as json_file:
        json.dump(config, json_file, indent=2)
    loggers.info("Downloads folder setted correctly to " + new_path)


def add_series(title, chapters_url):
    config["series"][title] = {"url": chapters_url, "downloaded_chapters": []}
    with open("settings.json", 'w') as json_file:
        json.dump(config, json_file, indent=2)
    loggers.info("Added " + title +
                 " to the downloads list. New chapters will be looked up at: " +
                 chapters_url)


def delete_series(title):
    config['series'].pop(title, None)
    with open("settings.json", 'w') as json_file:
        json.dump(config, json_file, indent=2)
    loggers.info("Deleted " + title + " from the downloads list.")


loggers: LoggerGroup

if __name__ == "__main__":
    loggers = LoggerGroup()
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    args = parser.parse_args()

    try:
        with open("settings.json", 'rb') as fp:
            config = json.load(fp)
    except FileNotFoundError:  # if file doesn't exists, starts with default values.
        config = {"downloads_folder": "C:\\tmp", "series": {}}
    try:
        if not args.Quiet:
            loggers.new_console_logger()
        if args.Logging:
            loggers.new_file_logger()
        if args.SetDownloadsFolder:
            set_downloads_folder(args.SetDownloadsFolder)
        if args.NewSeries:
            add_series(args.NewSeries[0], args.NewSeries[1])
        if args.Delete:
            delete_series(args.Delete)
        if args.Auto:
            if config["series"]:
                http = urllib3.PoolManager(
                    cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
                downloads_folder = config["downloads_folder"]
                series = config["series"]

                loggers.info("Mangoose started eating the mangoes.")
                eat()
                loggers.info("Mangoose finished eating the mangoes.")
            else:
                loggers.error(
                    "There are no mangoes for Mangoose to eat. Add them with -n MangaName MangaURL."
                )
    except Exception as e:
        print(e.__class__)
        loggers.error("Exception thrown at main")
