import requests, os, urllib, urllib2, string, base64, hashlib, random, re
from peewee import *
from bs4 import BeautifulSoup as soup
import bs4
from ...fields import CacheableFieldType, Cacher

def get_data_from_url(url_in):
    return requests.get(url_in).text

def get_soup_from_url(url_in):
    return soup(get_data_from_url(url_in))

wiktionary_en_raw = "http://en.wiktionary.org/wiki/{0}?printable=yes"

class GermanVerbixField(CacheableFieldType):
    db_name = 'de-verbix'
    anki_name = 'Meaning'

    def __init__(self,pathToDb):
        CacheableFieldType.__init__(self,pathToDb)
        self.verbixCache = Cacher(pathToDb,'de-verbix-pagestore')

    def generate(self,word):
        if self.verbixCache.exists(word):
            text = self.verbixCache.retrieve(word)
        else:
            url = 'http://www.verbix.com/webverbix/German/%s.html' % (word)
            text = requests.get(url).text
            self.verbixCache.store(word,text.encode('utf-8'))

        downloads_list = []

        word_soup = soup(text)

        # Gets the past participle
        pp = word_soup.findAll(attrs={'class': 'verbtable'})

        if len(pp) == 0:
            return None

        pp = pp[0].findAll('span')[-1]

        conj = pp.text.encode('utf-8')
        if pp['class'][0] == 'irregular':
            conj += '|I|'
        else:
            conj += '|R|'

        paragraphs = word_soup.findAll('p')
        if not paragraphs:
            raise Exception('No paragraphs')

        # Present er
        presentElem = paragraphs[1].findAll('span')[5]
        conj += presentElem.text.strip().encode('utf-8')
        if presentElem['class'][0] == 'irregular':
            conj += '|I|'
        else:
            conj += '|R|'

        # Perfect er
        perfectElem = paragraphs[2].findAll('span')[5]
        conj += perfectElem.text.strip().encode('utf-8')
        if perfectElem['class'][0] == 'irregular':
            conj += '|I|'
        else:
            conj += '|R|'

        # Past er
        pastElem = paragraphs[3].findAll('span')[5]
        conj += pastElem.text.strip().encode('utf-8')
        if pastElem['class'][0] == 'irregular':
            conj += '|I'
        else:
            conj += '|R'

        return conj