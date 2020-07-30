"""
Forvo isn't very forthcoming in offering a good, free API. (With good reason!)
This bypasses the need by parsing their site for audio files. I'd like to add
geolocation support someday (as they provide GPS coordinates for samples) to
deal with accents.
"""
import base64
import hashlib
import os
import random
import requests
import shutil
import string
import time
from urllib.parse import quote
from typing import List, Optional

from bs4 import BeautifulSoup as soup
from peewee import SqliteDatabase

from proto.transforms.base import Transform
from proto.field import FieldResult

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36"

HEADERS = {"User-Agent": UA}


def get_data_from_url(url_in: str) -> Optional[str]:
    times = 0
    sec = 5

    while True:
        text = ""
        failed = False
        try:
            text = requests.get(url_in, headers=HEADERS).text
        except:
            failed = True

        if not failed:
            return text

        times += 1

        # Sleep
        if times < 10:
            print("Call failed to %s." % url_in)
            time.sleep(pow(2, times) * sec)
        else:
            break

    return None


def get_soup_from_url(url_in):
    return soup(get_data_from_url(url_in), "html.parser")


BASE_URL = "https://audio00.forvo.com/"

"""Grabs audio for a given word in a target language from Forvo, a crowdsourced
pronunciation database."""


class Forvo(Transform[str]):
    def __init__(
        self,
        # ISO-639-1 language code
        language_code: str,
        # sleeps a little bit so that we don't ddos them
        throttle: bool = True,
        # If array is non-empty, limit sounds to the list of users
        limit_users: List[str] = [],
        # If array is non-empty, limit sounds to pronouncers from the English
        # name of the given countr(y/ies)"""
        limit_countries: List[str] = [],
    ):
        # Separate words from different languages in the database
        self.db_name = "forvo-" + language_code
        self.code = language_code
        self.throttle = throttle
        self.limit_countries = limit_countries
        self.limit_users = limit_users

    def call(self, word: str) -> FieldResult:
        """
        This code used to be way worse, trust me.
        This pulls the audio files.
        """
        downloads_list = []

        u_word = quote(word)

        target = self.code
        url = "http://www.forvo.com/word/%s/#%s" % (u_word, target)

        word_soup = get_soup_from_url(url)

        languages = word_soup.findAll(attrs={"class": "pronunciations"})

        for language in languages:
            abbrs = language.findAll("abbr")

            if len(abbrs) == 0:
                continue

            abbr = abbrs[0].contents[0]

            # Make sure we only get audio for the desired language
            if not abbr == target:
                continue

            pronunciations = language.findAll("ul")[0].findAll("li")

            # Iterate through all pronunciations
            for pron in pronunciations:
                if len(self.limit_countries) > 0:
                    # Check to see where the speaker is from
                    loc = pron.findAll(attrs={"class": "from"})

                    if not loc:
                        continue

                    loc = loc[0].contents[0]

                    # Splits the string and grabs just the last word
                    loc = loc.split()[-1][:-1]

                    # Skip the pronunciation
                    if not loc in self.limit_countries:
                        continue

                if len(self.limit_users) > 0:
                    # Find the username of this pronunciation
                    try:
                        usr = pron.findAll(attrs={"class": "uLink"})[0].contents[0]
                    except:
                        continue

                    # Skip the pronunciation if the name is not in the users list
                    if not usr in self.limit_users:
                        continue

                # Grab the sound
                a_list = pron.findAll("span", attrs={"class": "play"})
                for a in a_list:
                    try:
                        href = a["onclick"]
                    except KeyError:
                        continue

                    # construct the url again
                    parts = href.split(",")

                    if not "Play" in parts[0]:
                        continue

                    mp3_64 = parts[1][1:-1]
                    mp3_url = (BASE_URL + "mp3/{0}").format(
                        base64.b64decode(mp3_64).decode("utf-8")
                    )
                    downloads_list.append(mp3_url)
                    break

        # Clear out old downloads
        hashed = hashlib.md5(bytes(word, "utf-8")).hexdigest()

        if not downloads_list:
            return None

        first = downloads_list[0]
        filename = "%s.mp3" % (hashed)
        response = requests.get(first, headers=HEADERS)

        if self.throttle:
            time.sleep(1.0)

        return {
            "filename": filename,
            "field": "[sound:%s]" % filename,
            "data": response.content,
        }
