# -*- coding: utf-8 -*-
"""Starling is an online verb conjugator for Russian that doesn't distribute
any usable dataset. Instead, we just parse their online site to get
conjugations."""

from ...fields import FieldType, CacheableFieldType, Cacher

from bs4 import BeautifulSoup as soup
import bs4
import requests, urllib

starlingUrl = (
    "http://starling.rinet.ru/cgi-bin/morph.cgi?flags=endnnnnp&root=config&word="
)

vowels = ["а", "ю", "я", "и", "о", "ы", "у", "е"]


def replaceStress(word):
    """Changes Starling's manner of showing word stress on a vowel into a bolded
       vowel, which is much more aesthetically appealing."""

    # Iterates over all possible stressed vowels
    for vowel in vowels:
        stressed = vowel + "'"

        # Special case for the umlautted ye
        if vowel == "е":
            double = vowel + '"'
            if double in word:
                word = word.replace(double, "ё")
                continue

        if stressed in word:
            word = word.replace(stressed, "<b>%s</b>" % vowel)

    return word


def Starling_stripStress(word):
    """Strips all the stress marks from a word."""
    word = word.replace(u"\u0435''", u"\u0451")
    word = word.replace(u"\u0435'", u"\u0435")
    word = word.replace(u"\u0438'", u"\u0438")
    word = word.replace(u"\u0430'", u"\u0430")
    word = word.replace(u"\u043E'", u"\u043E")
    word = word.replace(u"\u0443'", u"\u0443")
    word = word.replace(u"\u044B'", u"\u044B")
    word = word.replace(u"\u044D'", u"\u044D")
    word = word.replace(u"\u044E'", u"\u044E")
    word = word.replace(u"\u044F'", u"\u044F")
    return word


class StarlingVerbField(CacheableFieldType):
    db_name = "starling-verb-ru"
    anki_name = "Conjugation"

    def __init__(self, db):
        CacheableFieldType.__init__(self, db)

        self.pageCache = Cacher(db, "starling-verb-pagestore-ru")

    def pull(self, word):
        if self.cacher.exists(word):
            result = self.cacher.retrieve(word)

            """This fixes the occasional issue where some banned symbols showed
               up in the database. I'm pretty sure it doesn't happen anymore but
               since pulling from the cache is so quick anyway I'll leave this
               here."""
            fixed = False
            for rem in ['"', "\n"]:
                if rem in result:
                    result = result.replace(rem, "")
                    fixed = True

            # If the data had to be fixed, store it in the cache again
            if fixed:
                self.cacher.store(word, result)

            return result

        # Otherwise, we'll have to generate the word
        result = self.generate(word)

        if not result:
            return None

        self.cacher.store(word, result)

        return result

    def generate(self, word):
        try:
            word = word.encode("utf-8")
        except:
            pass

        # Keeps a page cache of Starling so we don't always have to pull from it
        if self.pageCache.exists(word):
            pageText = self.pageCache.retrieve(word)
        else:
            # Starling uses some ancient encoding
            w1251 = urllib.quote_plus(word.decode("utf-8").encode("cp1251", "ignore"))

            # Create the full url
            url = starlingUrl + w1251

            try:
                r = requests.get(url)
            except:
                return None

            # Decode the page from utf-8
            pageText = r.text.encode("utf-8")

            self.pageCache.store(word, pageText)

        # The page source
        text = pageText

        # If the source is empty, something went wrong so we return None
        if text == "":
            return None

        # Creates a beautifulsoup of the page's source
        page = soup(text)

        # Grabs all the tables of declensions/conjugations
        tables = page.findAll("table")
        for table in tables:
            try:
                border = table["border"]
            except KeyError:
                continue

            rows = table.findAll("tr")
            # If there are four rows, we have a verb conjugation table
            if len(rows) == 4:
                # Delete the first row
                rows.pop(0)
                # All the conjugations
                cnj = []
                # Creates a list of all of the verb's conjugations
                try:
                    for row in rows:
                        contentRows = row.findAll("td")
                        for subRow in contentRows:
                            item = subRow.contents[0]
                            item = item.encode("cp1251", "ignore")
                            item = replaceStress(item)
                            cnj.append(item)
                except IndexError:
                    return None

                # We only care about a few of the conjugations
                conjString = "{0},{1},{2}".format(cnj[0], cnj[4], cnj[5])
                return conjString

        return None
