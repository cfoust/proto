# -*- coding: utf-8 -*-
from ...fields import FieldType, CacheableFieldType, Cacher

from bs4 import BeautifulSoup as soup
import bs4
import requests, urllib, random, os

wiktionary_en_raw = "http://ru.wiktionary.org/wiki/{0}?printable=yes"

class RuktionaryField(CacheableFieldType):
    db_name = 'conruktion'
    anki_name = 'Meaning'

    def __init__(self,pathToDb):
        CacheableFieldType.__init__(self,pathToDb)

        self.wikiCache = Cacher(pathToDb,'conwiktion-ru-wikistore')

    def generate(self,word):
        try:
            word = word.encode('utf-8')
        except:
            pass

        if self.wikiCache.exists(word):
            wikiText = self.wikiCache.retrieve(word)
        else:
            url = wiktionary_en_raw.format(urllib.quote(word))
            wikiText = requests.get(url).text
            self.wikiCache.store(word,wikiText.encode('utf-8'))

        text = wikiText

        if text == '':
            return None

        page = soup(text)

        zna = page.find(text='Значение')
        if zna == None:
            return ''
        ol = zna.findNext('ol')
        if not ol:
            return ''
        defs = []
        for defi in ol.findAll('li'):
            defs.append(defi.text)

        if len(defs) == 0:
            return ''

        total = ''

        for i,defi in enumerate(defs):
            defi = defi.encode('utf-8')
            if defi == '':
                continue
            if '◆' in defi:
                examples = defi.split('◆')
                if examples[0].strip() == '':
                    continue
                total += '%d. ' % (i+1)
                total += examples[0] + ' '
                for example in examples[1:]:
                    if example != '' and 'указан' not in example:
                        total += '◆ <i>%s</i> ' % example
            else:
                if 'указан' not in defi:
                    total += '%d. ' % (i+1)
                    total += defi + ' '

        if total != '':
            return total
        else:
            return None