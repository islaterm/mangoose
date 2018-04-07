#!/usr/bin/python
# coding=utf-8

"""
Mango eating mongoose.
"""
import json

import certifi as certifi
import os

__author__ = 'Ignacio Slater Muñoz'
__project__ = ""
__email__ = "islaterm@gmail.com"
__version__ = "0.0.001"

import urllib3
import requests
from bs4 import BeautifulSoup

http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())
with open("settings.json", 'r') as fp:
    config = json.load(fp)
downloads_folder = config["downloads_folder"]
series = config["series"]


def download(chapter, dest_path):
    i = 1
    while True:
        page_response = http.request('GET', chapter[1] + "/" + str(i))
        page_soup = BeautifulSoup(page_response.data, "html.parser")
        try:
            img_url = "https:" + page_soup.find('img', {"id": "manga-page"}).attrs['src']
        except AttributeError:  # Se llegó a la última página
            break
        print("Downloading " + chapter[0] + "; p" + str(i).zfill(3) + "...")
        response_image = requests.get(img_url, timeout=60)
        content_type = response_image.headers["Content-Type"]
        img_extension = content_type.split("/")[-1]
        file_name = "{0}.{1}".format(str(i).zfill(3), img_extension)
        filepath = os.path.join(dest_path, file_name)
        with open(filepath, 'wb') as img:
            img.write(response_image.content)
        i += 1
    return


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
        
        dir_path = os.path.join(downloads_folder, manga_name, chapter_title)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)
        
        download(chapter, dir_path)
        series[manga_name]["downloaded_chapters"].append(chapter_id)
        with open("settings.json", 'w') as json_file:
            json.dump(config, json_file)


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


if __name__ == "__main__":
    eat()
    print("Mangoose finished eating the mangoes.")
