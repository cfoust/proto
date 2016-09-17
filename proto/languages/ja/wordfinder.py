"""Takes in a string of kana (usually hiragana) and tries to find the 
corresponding word with kanji. Makes it so you can write down words phonetically
without having to enter the kanji. Then you can generate cards for them.

This is different from the field classes because those ones are optimized for 
lots of queries -- they make some shitty assumptions for the sake of speed. 

(i.e O(1) vs O(n))"""

from jmdictparse import *

import os, json

class WordFinder():

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
		self.dict = []

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

			self.dict.append(obj)

	def search(self, word):
		results = []

		for definition in self.dict:
			if word in definition['kanji'] or word in definition['kana']:
				results.append(definition)

		return results