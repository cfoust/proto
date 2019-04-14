"""Defines the different deck types for Mandarin."""

from ...deck import Deck
from ...fields import *
from ...cards import *


class WordCard(BasicCardType):
    name = 'zh-word'

    def __init__(self, db, partOfSpeech):
        headword = FieldType(True)
        headword.anki_name = "Headword"
        headword.html = '<div class="headword">%s</div>'

        sound = ForvoField(db, 'zh', limitCountries=['China'])
        sound.anki_name = "Sound"

        pos = StaticFieldType(partOfSpeech)
        pos.anki_name = "POS"
        pos.html = "<div style='display: none'>%s</div>"

        self.fields = [
            headword,
            sound,
            pos
        ]

        self.cards = []


class MandarinDeck(Deck):
	"""Deck for studying/learning radicals."""

	name = "Mandarin"

	csvname = 'zh'

	cardType = None

	subdecks = []

	def __init__(self, db):
		Deck.__init__(self)

		nouns = Deck()
		nouns.name = "Nouns"
		nouns.csvname = 'nouns'
		nouns.cardType = WordCard(db, 'noun')

		verbs = Deck()
		verbs.name = "Verbs"
		verbs.csvname = 'verbs'
		verbs.cardType = WordCard(db, 'verb')

		adjectives = Deck()
		adjectives.name = "Adjectives"
		adjectives.csvname = 'adj'
		adjectives.cardType = WordCard(db, 'adj')

		self.subdecks = [
			nouns,
			verbs,
			adjectives
		]
