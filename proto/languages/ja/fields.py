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

		# For entries that have exactly ONE kanji reading
		self.kanjiDict = {}

		# For entries that have exactly ONE kana reading
		self.kanaDict  = {}

		# Entries can be in either or both of above.

		# Every other entry.
		self.rest      = []

		numConflicts = 0

		for line in lines:
			parts = line.split('\t')

			# Parse the definitions
			defs = json.loads(parts[2])

			kanjiReadings = parts[0].split(',')
			# Filter out empty strings
			kanjiReadings = [x for x in kanjiReadings if not x == '']

			kanaReadings  = parts[1].split(',')
			# Filter out empty strings
			kanaReadings = [x for x in kanaReadings if not x == '']

			obj = {
				'kanji': kanjiReadings,
				'kana': kanaReadings,
				'defs': defs
			}

			if len(kanjiReadings) == 1:
				reading = kanjiReadings[0]
				# Check to see if there are any conflicts (same phrase)
				if reading in self.kanjiDict:
					if isinstance(self.kanjiDict[reading], list):
						self.kanjiDict[reading].append(obj)
					else:
						self.kanjiDict[reading] = [self.kanjiDict[reading], obj]

					numConflicts += 1
				else:
					self.kanjiDict[reading] = [obj]


			if len(kanaReadings) == 1:
				reading = kanaReadings[0]
				# Check to see if there are any conflicts (same phrase)
				if reading in self.kanaDict:
					if isinstance(self.kanaDict[reading], list):
						self.kanaDict[reading].append(obj)
					else:
						self.kanaDict[reading] = [self.kanaDict[reading], obj]
					numConflicts += 1
				else:
					self.kanaDict[reading] = [obj]

			self.rest.append(obj)

		# print "There were %d conflicts in the dictionary. (%d/%d/%d)" % (numConflicts, len(self.kanjiDict), len(self.kanaDict), len(self.rest))
	
	def getDefinitions(self, word):
		if word in self.kanjiDict:
			return json.dumps(self.kanjiDict[word])
		
		if word in self.kanaDict:
			return json.dumps(self.kanaDict[word])

		refs = []
		for entry in self.rest:
			if word in entry['kanji'] or word in entry['kana']:
				refs.append(entry)
		return json.dumps(refs)

	def pull(self,word):
		"""The code that looks through the dictionary is a little bit odd, but
		   the efficiency is definitely better than O(n). Just looks strange."""
		defs = self.getDefinitions(word)

		if len(defs) == 0:
			return None
		else:
			return defs