# -*- coding: utf-8 -*-
"""WikiInfo is a way of getting information about words by using (English)
Wiktionary's raw pages. They have a few macros for Russian words that give us
quick access to aspectual and word stress information."""

from ...fields import Cacher
from sdict import *
import requests, urllib, re, string

# Base url format
wiktionary_en_raw = "https://en.wiktionary.org/wiki/{0}?action=raw"

# We use this to check what SDict thinks about the aspect of a verb
sdict_template = "несовер\. \- ([^\s-]+)<br>совер\. \- ([^\s-]+)"

# Strips stress marks from Wiktionary's pages
def strip_stress(word):
    word = word.replace(u"\u0301","")
    word = word.replace('"','')
    word = word.replace('\n','')
    return word

class WikiInfo:
    def __init__(self,db,sdictPath):
        # Caches the lines that mentions a verb's aspect, pair, and stress
        self.stringCache = Cacher(db,'wiki-string-ru')

        # Caches the entire raw page
        self.pageCache = Cacher(db,'wiki-raw-page-ru')

        # Reference to the sDict dictionary
        self.sdict = SDictField(sdictPath)

    def getVerbLine(self,word):
        """Wiktionary has a particular line on the raw page for a Russian verb
           that has some really useful information about it. This function gets
           that line from the cache or from the raw page if necessary."""

        # Check if it's in the string/line cache
        wordString = self.stringCache.retrieve(word)
        if wordString:
            return wordString

        # Otherwise we check if the raw (full) page is in the page cache
        pageText = self.pageCache.retrieve(word)

        """At first glance, this seems stupid: why would we retun None if we
        have the page but no line for the word? It's because if we got the page
        at some point and don't have a word string, it means that the string
        wasn't found. In big databases that don't need to be updated this makes
        sense, but probably not that logical if we get better at parsing."""
        # todo: revisit this
        if pageText and not wordString:
            return None

        # Grabs the page if we don't have it
        if not pageText:
            try:
                word = word.encode('utf-8')
            except:
                pass
            url = wiktionary_en_raw.format(urllib.quote(word))
            try:
                pageText = requests.get(url).text
            except:
                return None

            # Stores the page in the cache
            self.pageCache.store(word,pageText.encode('utf-8'))

        # The raw text source
        text = pageText

        if text == '':
            return None

        # Split the page into lines
        lines = string.split(text,"\n")

        for line in lines:
            if not "ru-verb" in line:
                continue

            # ru-verb spotted
            # Look for it
            line = re.compile("{{([^\s]+)}}").search(line).group(1)
            # Got the line, store it
            # todo: might not have gotten the line
            self.stringCache.store(word,line)


            return line
        return None

    def getAspect(self,word):
        """Gets the aspect of a verb."""
        if not word:
            return None

        line = self.getVerbLine(word)
        if not line:
            # If we didn't find the line from Wiktionary, try with Starling
            try:
                word = word.encode('utf-8')
            except:
                pass
            definition = self.sdict.pull(word)
            if not definition:
                return None

            if "несовер.<br>" in definition:
                return 'impf'
            impf = "несовер. - " + word
            pf = "совер. - " + word

            if impf in definition:
                return "impf"
            else:
                return "pf"
        else:
            # We have a verb line, split by the pipe char
            fields = string.split(line,"|")

            # Return the third entry
            return fields[2].strip()

    def getStress(self,word):
        """Gets the stress of a verb."""

        line = self.getVerbLine(word)
        if not line:
            return word
        fields = string.split(line,"|")
        return fields[1]

    def getAspectualPair(self,word):
        """Gets the aspectual pair for the verb."""
        
        line = self.getVerbLine(word)

        if not line:
            return None

        fields = string.split(line,"|")
        if len(fields) > 3:
            part = fields[3]
            if "impf=" in part:
                return strip_stress(part[5:]).encode('utf-8')
            else:
                return strip_stress(part[3:]).encode('utf-8')

        definition = self.sdict.pull(word)

        if definition:
            p = re.compile(sdict_template)
            try:
                m = p.search(definition)
            except:
                return None

            imperfective = ""
            perfective = ""
            if m != None:
                imperfective = m.group(1)
                perfective = m.group(2)
                if imperfective == word:
                    return perfective
                else:
                    return imperfective

        
