# -*- coding: utf-8 -*-
"""File that describes all of the fields necessary for Japanese's cards."""

from ...fields import FieldType
from ...butils import fileLines
from jmdictparse import *

import os, json


class JMReadingField(FieldType):

	def __init__(self, furiFile):

		if not os.path.exists(furiFile):
			raise Exception("JMDict furigana file '%s' does not exist." % furiFile)

		"""Load the dict csv file and parse it into our dictionaries."""
		lines = fileLines(furiFile)

		# For entries that have exactly ONE kanji reading
		self.readingDict = {}

		numConflicts = 0

		for line in lines:
			parts = line.split('|')
			reading = parts[0]

			if reading in self.readingDict:
				self.readingDict[reading].append(line)
				numConflicts += 1
			else:
				self.readingDict[reading] = [line]

		# print "There were %d conflicts in the furigana." % numConflicts
	
	def getReadings(self, word):
		if word in self.readingDict:
			return self.readingDict[word]

		return []

	def pull(self,word):

		"""The code that looks through the dictionary is a little bit odd, but
		   the efficiency is definitely better than O(n). Just looks strange."""
		defs = self.getReadings(word)

		if len(defs) == 0:
			return ''
		else:
			return json.dumps(defs)

class JMDictField(FieldType):

	def __init__(self, dictFile):

		if not os.path.exists(dictFile):
			raise Exception("JMDict file '%s' does not exist." % dictFile)
		
		# Check to see whether the dictionary has been parsed and parses it
		# if it hasn't
		if not os.path.exists(dictFile + '.csv'):
			print "JMDict dictionary file has not been parsed into csv. Parsing."
			parseToFile(dictFile, dictFile + '.csv')
			print "Done parsing."

		"""Load the dict csv file and parse it into our dictionaries."""
		lines = fileLines(dictFile + '.csv')

		# Sucks to suck. We had to switch to an O(n) algorithm for dictionary
		# lookups because there's really no clean way to make it a hashmap.
		# 
		# I may revisit this if it becomes too slow. Japanese is not very
		# polysemous, so we could conjure some kind of key-value lookup
		# where multiple keys point to the same value. For now, this is fine.
		self.dictionary = []

		for line in lines:
			self.dictionary.append(json.loads(line))

	
	def getDefinitions(self, word):
		results = []

		try:
			word = word.decode('utf-8')
		except:
			pass
	
		for definition in self.dictionary:
			for reading in definition['readings']:
				if word == reading['kana'] or word == reading['kanji']:
					results.append(definition)
					break

		results = sorted(results, key=lambda d: d['score'], reverse=True)

		return results

	def pull(self,word):
		"""The code that looks through the dictionary is a little bit odd, but
		   the efficiency is definitely better than O(n). Just looks strange."""
		defs = self.getDefinitions(word)

		if len(defs) == 0:
			return None
		else:
			return json.dumps(defs)