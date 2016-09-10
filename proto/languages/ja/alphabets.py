from ...deck import Deck
from cards import *

"""Defines the different deck types for all the alphabets."""

class RadicalDeck(Deck):
	"""Deck for studying/learning radicals."""

	name = "Radicals"

	# This is the base CSV name we use to hold data to be imported into Anki
	csvname = 'radicals'

	cardType = None

	subdecks = []

	def __init__(self):
		Deck.__init__(self)

		meaning = Deck()
		meaning.name = "Meaning"
		meaning.csvname = 'meaning'
		meaning.cardType = RadicalInfo()

		stroke = Deck()
		stroke.name = "Stroke"
		stroke.csvname = 'stroke'
		stroke.cardType = RadicalStroke()

		self.subdecks = [
			meaning,
			stroke
		]

class PhoneticDeck(Deck):
	"""Deck for studying/learning a phonetic alphabet."""

	cardType = None

	subdecks = []

	def __init__(self, db):
		Deck.__init__(self)

		# Makes its symbol to sound deck
		sound = Deck()
		sound.name = "Sound"
		sound.csvname = 'symbol-to-sound'
		sound.cardType = SymbolToSoundCard(db)

		stroke = Deck()
		stroke.name = "Stroke"
		stroke.csvname = 'sound-to-stroke'
		stroke.cardType = SoundToStrokeCard(db)

		self.subdecks = [
			sound,
			stroke
		]


class AlphabetsDeck(Deck):
	"""Deck for studying/learning Hiragana, Katakana, and radicals."""

	name = "Alphabets"

	# This is the base CSV name we use to hold data to be imported into Anki
	csvname = 'alphabets'

	cardType = None

	subdecks = []

	def __init__(self, db):
		Deck.__init__(self)

		# Creates the main hiragana deck
		hiragana = PhoneticDeck(db)
		hiragana.name = "Hiragana"
		hiragana.csvname = "hiragana"

		katakana = PhoneticDeck(db)
		katakana.name = "Katakana"
		katakana.csvname = "katakana"
		
		radicals = RadicalDeck()

		self.subdecks = [
			hiragana,
			katakana,
			radicals
		]