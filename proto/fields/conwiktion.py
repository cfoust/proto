"""Conwiktion is a field type that parses wiktionary for results."""

import requests, os, urllib, urllib2, string, base64, hashlib, time, random, re
from peewee import *
from bs4 import BeautifulSoup as soup
import bs4
from basic import CacheableFieldType, Cacher

def get_data_from_url(url_in):
	return requests.get(url_in).text

def get_soup_from_url(url_in):
	return soup(get_data_from_url(url_in))


"""The secret to parsing wiktionary (or Wikipedia) is to never parse it at all.
As you can tell, the code below is pretty messy but works. It's a relic from
my first attempts at generating flash cards in 8/13."""

wiktionary_en_raw = "http://en.wiktionary.org/wiki/{0}?printable=yes"

class WiktionaryField(CacheableFieldType):
	db_name = 'conwiktion'
	anki_name = 'Meaning'

	def __init__(self,db,languageName,languageCode):
		self.db_name = self.db_name + '-' + languageCode.lower()
		CacheableFieldType.__init__(self,db)
		self.languageName = languageName
		
		self.wikiCache = Cacher(db,'conwiktion-wikistore')

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

		# Lets us see relative element ordering because Wiktionary's is awful
		container = page.find(id='mw-content-text')
		def comesBefore(left,right):
			if left == right:
				return False
			for element in container:
				if left == element:
					return True
				elif right == element:
					return False

		# Establish the top and bottom elements
		zna = page.find(id=self.languageName)
		if not zna:
			return None
		lower = zna.findNext('hr')
		if not lower or not comesBefore(zna.parent,lower):
			lower = zna.findNext('h2')
			if not lower:
				for e in container:
					lower = e

		# Check if there are multiple etymologies

		etymologies = []

		multi = zna.findNext('span',text=re.compile('^Etymology [\d]+'))
		if zna.findNext('span',text='Etymology'):
			e = zna.findNext('span',text='Etymology')

			if comesBefore(e.parent,lower):
				etymologies.append(e)
			else:
				return None
		elif multi:
			index = 1
			while True:
				e = zna.findNext('span',text='Etymology %d' % index)

				if not e:
					break

				if comesBefore(e.parent,lower):
					etymologies.append(e)
				else:
					break

				index += 1
		else: # No etymology
			etymologies.append(zna)
		
		totalDefs = 0
		total = ''
		for pos in ['Adjective','Noun','Verb']:
			definitions = []
			for i,ety in enumerate(etymologies):
				if pos == 'Adjective':
					ele = ety.findNext('span',text='Adjective')
				elif pos == 'Noun':
					ele = ety.findNext('span',text='Noun')
				elif pos == 'Verb':
					ele = ety.findNext('span',text='Verb')

				if not ele:
					continue

				if i < (len(etymologies) - 1):
					if not comesBefore(ele.parent,etymologies[i+1].parent):
						continue
				else:
					if not comesBefore(ele.parent,lower):
						continue

				ol = ele.findNext('ol')

				for defi in ol.findAll('li'):
					fixed = ''

					# Past Caleb, you are so lame
					for item in defi.contents:
						if type(item) == bs4.element.NavigableString:
							fixed += item
						elif type(item) == bs4.element.Tag:
							if item.name in ['a','span','i','b']:
								fixed += item.text
							elif item.name == 'dl': # an example
								for ep in item.dd.contents:
									if ep.name == 'i':
										fixed += str(ep).decode('utf-8')
									elif ep.name == 'dl':
										fixed += ' ' + ep.dd.text
					definitions.append(fixed)

			if len(definitions) == 0:
				continue

			totalDefs += len(definitions)

			lines = []

			if len(definitions) == 1:
				defi = definitions[0].encode('utf-8')
				lines.append(defi)
			else:
				for i,defi in enumerate(definitions):
					defi = defi.encode('utf-8')
					line = '%d. %s' % (i+1,defi)
					lines.append(line)

			total += '<b>' + pos + '</b><br>'
			total += '<br>'.join(lines)

		if totalDefs == 0:
			return None

		total = string.replace(total,'\t','')
		total = string.replace(total,'\n','<br>')

		return total