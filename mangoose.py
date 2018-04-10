#!/usr/bin/python
# coding=utf-8

"""
Mango eating mongoose.
"""
import argparse
import json
import logging
import os
from logging.handlers import RotatingFileHandler

import certifi as certifi
import requests
import urllib3
from bs4 import BeautifulSoup

__author__ = 'Ignacio Slater Muñoz'
__project__ = "Mangoose"
__email__ = "islaterm@gmail.com"
__version__ = "0.0.005"


# TODO 0 -cAdd : Add new series via cmd.
# TODO 0 -cAdd : Auto and manual download modes.
# TODO 1 -cAdd : More sources.


def setup_logger(a_logger, log_to_std, log_to_file):
    a_logger.setLevel(logging.INFO)
    if log_to_file:
        log_file_handler = RotatingFileHandler(filename='mangoose.log', maxBytes=50000, backupCount=1)
        log_file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
        a_logger.addHandler(log_file_handler)
    if log_to_std:
        log_std_handler = logging.StreamHandler()
        log_std_handler.setFormatter(logging.Formatter('%(message)s'))
        a_logger.addHandler(log_std_handler)


def validate(title):
    title = title.replace(": ", " - ").replace(':', '-').replace('?', '_').replace('/', '_')
    return title


def download(chapter, dest_path):
    i = 1
    while True:
        page_response = http.request('GET', chapter[1] + "/" + str(i))
        page_soup = BeautifulSoup(page_response.data, "html.parser")
        try:
            img_url = "https:" + page_soup.find('img', {"id": "manga-page"}).attrs['src']
        except AttributeError:  # Se llegó a la última página
            break
        logger.info("Downloading " + chapter[0] + "; p" + str(i).zfill(3) + "...")
        response_image = requests.get(img_url, timeout=60)
        content_type = response_image.headers["Content-Type"]
        img_extension = content_type.split("/")[-1]
        file_name = "{0}.{1}".format(str(i).zfill(3), img_extension)
        filepath = os.path.join(dest_path, file_name)
        with open(filepath, 'wb') as img:
            img.write(response_image.content)
        i += 1


def eat():
    for title in series:
        eat_mango(title, series[title]["url"], series[title]["downloaded_chapters"])


def eat_mango(manga_name: str, manga_url: str, skip=None):
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
        
        dir_path = os.path.join(downloads_folder, validate(manga_name), validate(chapter_title))
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        download(chapter, dir_path)
        series[manga_name]["downloaded_chapters"].append(chapter_id)
        with open("settings.json", 'w') as json_file:
            json.dump(config, json_file, indent=2)


def parse_table(table):
    entries = []
    for element in table:
        url_prefix = "https://readms.net" + "/".join(element.attrs['href'].split('/')[:-1])
        entries.append((element.contents[0], url_prefix))
    return entries


def get_chapters(soup_url: BeautifulSoup):
    chapters_table = soup_url.find("table", {"class": "table table-striped"})
    chapters = parse_table(chapters_table.find_all("a"))
    return chapters


def setup_parser(a_parser):
    a_parser.add_argument("-d", "--SetDownloadsFolder", help="Sets the destination folder for the downloaded mangas.")
    a_parser.add_argument("-l", "--Logging", help="Writes execution info to a file.", action="store_true",
                          default=False)
    a_parser.add_argument("-q", "--Quiet", help="Turns off std out printing.", action="store_true", default=False)


def set_downloads_folder(new_path):
    new_path = os.path.normpath(new_path)
    if not os.path.isdir(new_path):
        os.makedirs(new_path)
        logger.info("Created directory " + new_path)
    config["downloads_folder"] = new_path
    with open("settings.json", 'w') as json_file:
        json.dump(config, json_file, indent=2)
    logger.info("Downloads folder setted correctly to " + new_path)


if __name__ == "__main__":
    logger = logging.getLogger("mangoose")
    parser = argparse.ArgumentParser()
    setup_parser(parser)
    args = parser.parse_args()
    
    with open("settings.json", 'r') as fp:
        config = json.load(fp)
    try:
        setup_logger(logger, log_to_std=not args.Quiet, log_to_file=args.Logging)
        if args.SetDownloadsFolder:
            set_downloads_folder(args.SetDownloadsFolder)
        
        http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
        downloads_folder = config["downloads_folder"]
        series = config["series"]
        
        logger.info("Mangoose started eating the mangoes.")
        eat()
        logger.info("Mangoose finished eating the mangoes.")
    except Exception as e:
        print(e.__class__)
        logger.exception("Exception thrown at main")
