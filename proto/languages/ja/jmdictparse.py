"""Parses a JMDict file into a .csv file."""

from ...butils import *
import json, codecs
# Need some beautfiul soup for this
from bs4 import BeautifulSoup as soup

def parseEntry(entryString):
	# Parse the entry from its HTML
	entrySoup = soup(entryString, 'html.parser')

	# Look for all the kanji readings
	kanjiReadings = []
	for r in entrySoup.findAll('k_ele'):
		kanjiReadings.append(r.findAll('keb')[0].contents[0])

	# Look for all the kana readings
	kanaReadings = []
	for r in entrySoup.findAll('r_ele'):
		kanaReadings.append(r.findAll('reb')[0].contents[0])

	# Parse all of the senses
	senses = []
	for sense in entrySoup.findAll('sense'):

		# Gather the misc for the sense
		miscs = []
		for misc in sense.findAll('misc'):
			miscs.append(misc.contents[0])

		# Gather the pos for the sense
		poses = []
		for pos in sense.findAll('pos'):
			poses.append(pos.contents[0])

		# Get the glosses too
		glosses = []
		for gloss in sense.findAll('gloss'):
			glosses.append(gloss.contents[0])

		senses.append({
			'tags': miscs,
			'pos': poses,
			'glosses': glosses
		})

	obj = {
		'kanji': kanjiReadings,
		'kana': kanaReadings,
		'defs': senses
	}
	return obj

def parseToFile(jmDict, out):
	# Gets the lines of the dictionary
	dictLines = fileLines(jmDict)

	outFile = codecs.open(out, 'w', 'utf-8')

	num = 0

	index = 0
	while True:
		if index >= len(dictLines):
			break

		# Store the current line
		line = dictLines[index]

		# If it's not the start of an entry, continue
		if line != '<entry>':
			index += 1
			continue
		
		# Start looking one line ahead
		searchIndex = index + 1
		
		# Store the end index
		foundEnd = False
		endIndex = -1

		# Look for where the entry definition ends
		while True:
			if searchIndex >= len(dictLines):
				break

			searchLine = dictLines[searchIndex]

			if searchLine == "</entry>":
				endIndex = searchIndex
				foundEnd = True
				break

			searchIndex += 1

		# If we didn't find the end of the entry definition, continue.
		if not foundEnd:
			index += 1
			continue

		entry = '\n'.join(dictLines[index : endIndex + 1])
		parsed = parseEntry(entry)
		parsedArray = [
			','.join(parsed['kanji']),
			','.join(parsed['kana']),
			json.dumps(parsed['defs'])
		]
		outFile.write('\t'.join(parsedArray) + '\n')

		index += 1