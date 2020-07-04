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

from bs4 import BeautifulSoup as soup

from proto import Field


def get_data_from_url(url_in):
    times = 0
    sec = 5
    while True:
        text = ""
        failed = False
        try:
            text = requests.get(url_in).text
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


def get_soup_from_url(url_in):
    return soup(get_data_from_url(url_in), "html.parser")


BASE_URL = "https://audio00.forvo.com/"

"""Grabs audio for a given word in a target language from Forvo, a crowdsourced
pronunciation database."""


class Forvo(Field[str]):
    db_name = "forvocate"
    anki_name = "Audio"
    html = """%s"""

    def __init__(
        self,
        db,
        languageCode,
        storagePath=None,
        outputPath=None,
        throttle=True,
        soundCap=1,
        randomSound=False,
        limit_users=[],
        limitCountries=[],
    ):
        """db: database
           languageCode: ISO-639-1 language code
           outputPath: folder to put the media files (.mp3) in
           throttle: sleeps a little bit so that we don't ddos them
           soundCap: number of sounds to grab (usually 1)
           randomSound: if there are many sounds on the page for the word,
                        grab one randomly
           limit_users: If array is non-empty, limit sounds to the list of users
           limitCountries: If array is non-empty, limit sounds to pronouncers
                           from the English name of the given countr(y/ies)"""

        # Separate words from different languages in the database
        self.db_name = self.db_name + "-" + languageCode

        self.optional = True

        CacheableFieldType.__init__(self, db)

        self.code = languageCode

        self.throttle = throttle
        self.soundCap = soundCap
        self.randomSound = randomSound
        self.limitCountries = limitCountries
        self.limit_users = limit_users

        if not storagePath:
            self.storage_path = "forvocate/" + languageCode + "/"
        else:
            self.storage_path = storagePath

        if not os.path.exists(self.storage_path):
            os.makedirs(self.storage_path)

        if not outputPath:
            self.output_path = "media/" + languageCode + "/"
        else:
            self.output_path = outputPath

        # Create the output dir if it doesn't exist
        if not os.path.exists(self.output_path):
            os.makedirs(self.output_path)

    def pull(self, word):
        result = CacheableFieldType.pull(self, word)

        if not result:
            """It doesn't matter if this field has nothing, so we return a blank
               string. We do this because it's not a dealbreaker if a card has
               no sound."""
            return None

        # Deal with fucking Python encoding
        try:
            word = word.encode("utf-8")
        except:
            pass

        """Generates the resulting file paths based on the number of sounds we stored.
           We don't really care about using hash here as even big decks have only
           30k or so cards. Not worth worrying about conflicts. """
        results = [
            hashlib.md5(word).hexdigest() + str(x) + ".mp3" for x in range(int(result))
        ]

        if len(results) == 0:
            return None

        # Choose a random sound, otherwise just grab the first one
        if self.randomSound:
            choice = random.choice(results)
        else:
            choice = results[0]

        # Only copy in the file if it's not already there
        if not os.path.exists(self.output_path + choice):
            shutil.copyfile(self.storage_path + choice, self.output_path + choice)

        # This is the format Anki understands to play a sound
        return "[sound:%s]" % choice

    def generate(self, word):
        """This code used to be way worse, trust me.
           This pulls the audio files."""
        downloads_list = []

        try:
            word = word.encode("utf-8")
        except:
            pass

        u_word = quote(word)

        language = "en"
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
                if len(self.limitCountries) > 0:
                    # Check to see where the speaker is from
                    loc = pron.findAll(attrs={"class": "from"})

                    if not loc:
                        continue

                    loc = loc[0].contents[0]

                    # Splits the string and grabs just the last word
                    loc = loc.split()[-1][:-1]

                    # Skip the pronunciation
                    if not loc in self.limitCountries:
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
        hashed = hashlib.md5(word).hexdigest()
        index = 0
        while os.path.isfile(self.storage_path + hashed + str(index) + ".mp3"):
            os.remove(self.storage_path + hashed + str(index) + ".mp3")
            index += 1

        # Download the new sounds
        for i, url in enumerate(downloads_list):
            if i == self.soundCap:
                break
            r = requests.get(url)
            with open(self.storage_path + hashed + str(i) + ".mp3", "wb") as code:
                code.write(r.content)
            if self.throttle:
                time.sleep(1.0)

        numSounds = min(len(downloads_list), self.soundCap)
        if numSounds == 0:
            return None
        else:
            return str(numSounds)
