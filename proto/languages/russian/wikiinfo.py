# -*- coding: utf-8 -*-
from ...fields import Cacher
from sdict import *
import requests, urllib, re, string

wiktionary_en_raw = "http://en.wiktionary.org/wiki/{0}?action=raw"
sdict_template = "несовер\. \- ([^\s-]+)<br>совер\. \- ([^\s-]+)"

def strip_stress(word):
	word = word.replace(u"\u0301","")
	word = word.replace('"','')
	word = word.replace('\n','')
	return word

class WikiInfo:
	def __init__(self,pathToDb,sdictPath):
		self.stringCache = Cacher(pathToDb,'wiki-string-ru')
		self.pageCache = Cacher(pathToDb,'wiki-raw-page-ru')
		self.sdict = SDictField(sdictPath)

	def getVerbLine(self,word):

		wordString = self.stringCache.retrieve(word)
		if wordString:
			return wordString

		pageText = self.pageCache.retrieve(word)
		if pageText and not wordString:
			return None
		if not pageText:
			try:
				word = word.encode('utf-8')
			except:
				pass
			url = wiktionary_en_raw.format(urllib.quote(word))
			pageText = requests.get(url).text
			self.pageCache.store(word,pageText.encode('utf-8'))

		text = pageText

		if text == '':
			return None

		lines = string.split(text,"\n")
		for line in lines:
			if "ru-verb" in line:
				line = re.compile("{{([^\s]+)}}").search(line).group(1)

				self.stringCache.store(word,line)
				
				return line
		return None

	def getAspect(self,word):
		if not word:
			return None
		line = self.getVerbLine(word)
		if line == None:
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
			fields = string.split(line,"|")
			return fields[2]

	def getStress(self,word):
		line = self.getVerbLine(word)
		if not line:
			return word
		fields = string.split(line,"|")
		return fields[1]

	def getAspectualPair(self,word):
		definition = self.sdict.pull(word)
		
		if definition:
			p = re.compile(sdict_template)
			try: 
				m = p.search(definition)
			except:
				return None

			imperfective = ""
			perfective = ""
			if m == None:
				return None
			else:
				imperfective = m.group(1)
				perfective = m.group(2)
				if imperfective == word:
					return perfective
				else:
					return imperfective

		line = self.getVerbLine(word)
		
		if not line:
			return None

		fields = string.split(line,"|")
		if len(fields) > 3:
			part = fields[3]
			if "impf=" in part:
				return strip_stress(part[5:]);
			else:
				return strip_stress(part[3:]);
