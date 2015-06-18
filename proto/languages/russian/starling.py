# -*- coding: utf-8 -*-
from ...fields import FieldType, CacheableFieldType, Cacher

from bs4 import BeautifulSoup as soup
import bs4
import requests, urllib

starlingUrl = "http://starling.rinet.ru/cgi-bin/morph.cgi?flags=endnnnnp&root=config&word="

vowels = ['а', 'ю', 'я', 'и', 'о', 'ы', 'у', 'е']
def replaceStress(word):
	for vowel in vowels:
		stressed = vowel + "'"
		if vowel == 'е':
			double = vowel + '"'
			if double in word:
				word = word.replace(double,'ё')
				continue
		if stressed in word:
			word = word.replace(stressed,'<b>%s</b>' % vowel)
	return word


def Starling_stripStress(word):
	word = word.replace(u"\u0435''",u"\u0451")
	word = word.replace(u"\u0435'",u"\u0435")
	word = word.replace(u"\u0438'",u"\u0438")
	word = word.replace(u"\u0430'",u"\u0430")
	word = word.replace(u"\u043E'",u"\u043E")
	word = word.replace(u"\u0443'",u"\u0443")
	word = word.replace(u"\u044B'",u"\u044B")
	word = word.replace(u"\u044D'",u"\u044D")
	word = word.replace(u"\u044E'",u"\u044E")
	word = word.replace(u"\u044F'",u"\u044F")
	return word


class StarlingVerbField(CacheableFieldType):
	db_name = 'starling-verb-ru'
	anki_name = 'Conjugation'

	def __init__(self,pathToDb):
		CacheableFieldType.__init__(self,pathToDb)
		
		self.pageCache = Cacher(pathToDb,'starling-verb-pagestore-ru')

	def pull(self,word):
		if self.cacher.exists(word):
			result = self.cacher.retrieve(word)

			fixed = False
			for rem in ['"','\n']:
				if rem in result:
					result = result.replace(rem,'')
					fixed = True
			
			if fixed:
				self.cacher.store(word,result)
			
			return result
		else:
			result = self.generate(word)

			if not result:
				return None

			self.cacher.store(word,result)
			return result

	def generate(self,word):
		try:
			word = word.encode('utf-8')
		except:
			pass

		if self.pageCache.exists(word):
			pageText = self.pageCache.retrieve(word)
		else:
			w1251 = urllib.quote_plus(word.decode('utf-8').encode('cp1251','ignore'))
			url = starlingUrl + w1251
			r = requests.get(url)
			pageText = r.text.encode('utf-8')
			self.pageCache.store(word,pageText)

		text = pageText

		
		if text == '':
			return None

		page = soup(text)

		tables = page.findAll('table')
		for table in tables:
			try:
				border = table['border']
			except KeyError:
				continue
			rows = table.findAll('tr')
			if (len(rows) == 4):
				rows.pop(0)
				cnj = []
				try:
					for row in rows:
						contentRows = row.findAll('td')
						for subRow in contentRows:
							item = subRow.contents[0]
							item = item.encode('cp1251','ignore')
							item = replaceStress(item)
							cnj.append(item)
				except IndexError:
					return None
				
				conjString = "{0},{1},{2}".format(cnj[0],cnj[4],cnj[5])
				return conjString
			else:
				continue

		return None