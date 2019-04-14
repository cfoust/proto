from ...deck import Deck
from cards import *

class WordsDeck(Deck):
	"""Deck for studying/learning radicals."""

	name = "Words"

	# This is the base CSV name we use to hold data to be imported into Anki
	csvname = 'words'

	cardType = None

	subdecks = []

	def __init__(self, db, dictFile, furiFile):
		Deck.__init__(self)

		nouns = Deck()
		nouns.name = "Nouns"
		nouns.csvname = 'nouns'
		nouns.cardType = WordCard(db, dictFile, furiFile, 'noun')

		verbs = Deck()
		verbs.name = "Verbs"
		verbs.csvname = 'verbs'
		verbs.cardType = WordCard(db, dictFile, furiFile, 'verb')

		adjectives = Deck()
		adjectives.name = "Adjectives"
		adjectives.csvname = 'adj'
		adjectives.cardType = WordCard(db, dictFile, furiFile, 'adj')

		self.subdecks = [
			nouns,
			verbs,
			adjectives
		]