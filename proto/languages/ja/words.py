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
		nouns.cardType = NounCard(db, dictFile, furiFile)

		self.subdecks = [
			nouns
		]