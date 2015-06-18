from butils import *
from proto.exporters import APKGExporter,CSVExporter

"""Why do we do it this way? I dunno, it's a little messy but the abstraction
it gives is so much better. Each deck builder just takes in data and changes
the templates a bit. No need to include all the iteration code each time."""
class Builder:
	headDeck = None
	languageCode = None
	deckTree = {}


	def __init__(self,languageCode,deck):
		self.languageCode = languageCode
		self.ph = PathHelper(languageCode)
		self.headDeck = deck
		self.makeTree()

	def makeTree(self):
		neededFiles = self.ph.neededFiles(self.headDeck)
		def appendDeck(parentName,parentCsvName,deck):

			name = parentName + '::' + deck.name if parentName != '' else deck.name
			csvname = parentCsvName + '-' + deck.csvname if parentCsvName != '' else deck.csvname

			needData = csvname + '.csv' in neededFiles
			self.deckTree[name] = {
				'csvname': csvname,
				'needData': needData,
				'deck': deck,
				'data': []
			}
			for subdeck in deck.subdecks:
				appendDeck(name,csvname,subdeck)

		appendDeck('','',self.headDeck)

	def deckNeedsData(self,deckName):
		if not deckName in self.deckTree:
			raise Exception('No such deck: %s' % deckName)

		deckObject = self.deckTree[deckName]['needData']
		return deckObject['needData'] and len(deckObject['data']) == 0

	def needAnyData(self):
		for deck in self.deckTree:
			if self.deckTree[deck]['needData']:
				return True
		return False

	def bindDeckData(self,deckName,data):
		if not deckName in self.deckTree:
			raise Exception('No such deck: %s' % deckName)

		self.deckTree[deckName]['data'] = data

	def build(self):
		for deckName in self.deckTree:
			deckObject = self.deckTree[deckName]
			name = deckName
			deck = deckObject['deck']
			data = deckObject['data']

			if not deckObject['needData']:
				print 'Skipping build for deck %s, either does not need data or already built.' % name
				continue

			if len(data) == 0:
				raise Exception('Deck %s needs data and has none.' % name)

			print 'Building cards for deck %s.' % name

			nones = 0
			for word in Progress(deckObject['data']):
				result = deck.makeCard(word)
				if None in result:
					nones += 1
			print 'Generated %d/%d cards.' % (len(data)-nones,len(data))
			CSVExporter.export(deck,self.ph.output + deckObject['csvname'] + '.csv')
		self.ph.apkgExport(self.headDeck)
		print 'Build of %s successful.' % self.headDeck.name