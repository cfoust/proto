from proto.butils import *
from proto.builder import *

from proto.languages.ru import *
from proto.languages.ru.wikiinfo import WikiInfo
from proto.exporters import CSVExporter, APKGExporter
from proto.importers import CSVImporter

oi = PathHelper('ru')
ph = PathHelper('ruru')

rd = RussianDeck(oi.db,oi.ifile('rus_eng_full2.dct'))
rd.name = "RussianRu"

CSVImporter.importIntoDeck(rd.subDeckByName('Nouns'),oi.ofile('ru-nouns.csv'))
CSVImporter.importIntoDeck(rd.subDeckByName('Verbs'),oi.ofile('ru-verbs.csv'))
CSVImporter.importIntoDeck(rd.subDeckByName('Adjectives'),oi.ofile('ru-adjectives.csv'))

types = [
	# ('Nouns','ru-nouns.csv'),
	# ('Verbs','ru-verbs.csv'),
	# ('Adjectives','ru-adjectives.csv')
]

for t,csvname in types:
	deck = rd.subDeckByName(t)
	ct = deck.cardType
	if t == 'Verbs':
		ct.fields[2] = RuktionaryField(oi.db)
		for card in ct.cards:
			card[2] = None
	else:
		ct.fields[1] = RuktionaryField(oi.db)
		for card in ct.cards:
			card[1] = None

	cards = ct.cards
	ct.cards = []

	print 'Filling in new data for %s.' % t
	if t == 'Verbs':
		for card in Progress(cards):
			if card[0]:
				word = card[0]
			elif card[1]:
				word = card[1]
			else:
				continue
			ct.fillIn(word,card)
	else:
		for card in Progress(cards):
			ct.fillIn(card[0],card)

	CSVExporter.export(deck,ph.output + csvname + '.csv')

ph.apkgExport(rd,ignoreMedia = True)