# -*- coding: utf-8 -*-
"""This shitshow of code parses the Russian version of wiktionary. They use a
   very different template so we cannot just use conwiktion. """

from ...fields import FieldType, CacheableFieldType, Cacher

from bs4 import BeautifulSoup as soup
import bs4
import requests, urllib, random, os

wiktionary_en_raw = "http://ru.wiktionary.org/wiki/{0}?printable=yes"

class RuktionaryField(CacheableFieldType):
    """Grabs data from ru.wiktionary.org for Russian definitions."""
    db_name = 'conruktion'
    anki_name = 'Meaning'

    def __init__(self,db):
        CacheableFieldType.__init__(self,db)

        self.wikiCache = Cacher(db,'conwiktion-ru-wikistore')

    def generate(self,word):
        try:
            word = word.encode('utf-8')
        except:
            pass

        # Checks whether we have a cache of the page we can use
        if self.wikiCache.exists(word):
            wikiText = self.wikiCache.retrieve(word)
        # If there is no page cache, grab it
        else:
            url = wiktionary_en_raw.format(urllib.quote(word))
            wikiText = requests.get(url).text
            self.wikiCache.store(word,wikiText.encode('utf-8'))

        # Source of the wiki page
        text = wikiText

        if text == '':
            return None

        # Create a beautifulsoup for the page
        page = soup(text)

        # Look for the meaning subsection
        zna = page.find(text='Значение')

        # If we couldn't find it, return nothing
        if zna == None:
            return None

        # Otherwise, look for the next definition list
        ol = zna.findNext('ol')

        # If we couldn't find it, return nothing
        if not ol:
            return None

        """ Create a provincial list of definitions by iterating over child
            elements"""
        defs = []
        for defi in ol.findAll('li'):
            defs.append(defi.text)

        # If we have no definitions, return None
        if len(defs) == 0:
            return None

        # Stores the formatted definition text
        total = ''

        """Iterate over all the definitions and pack it into a nice-looking
           numbered definition. """
        for i,defi in enumerate(defs):
            
            defi = defi.encode('utf-8')

            # If we find no definition there, continue
            if defi == '':
                continue
            
            # Checks if a symbol indicating an example of usage is present
            if '◆' in defi:
                # Gets a list of examples for this sub-definition.
                examples = defi.split('◆')
                
                """examples[0] will be the actual definition, and all other list
                   elements are examples. If examples[0] is empty, we skip this
                   sub-definition."""
                if examples[0].strip() == '':
                    continue

                # Append the actual sub-definition
                total += '%d. %s ' % ((i+1), examples[0])

                # Append all the examples, skipping the first element
                for example in examples[1:]:
                    if example != '' and 'указан' not in example:
                        total += '◆ <i>%s</i> ' % example
            # Since we have no examples, just add the definition.
            else:
                if 'указан' not in defi:
                    total += '%d. %s ' % ((i+1), defi)

        """Return None if total has nothing, otherwise just return the formatted
          definition"""
        if total != '':
            return total
        else:
            return None