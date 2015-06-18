from ...deck import Deck


from cards import *


class RussianVerbsDeck(Deck):
	name = "Verbs"
	csvname = 'verbs'
	cardType = None

	def __init__(self,pathToDb,pathToSdict):
		self.cardType = RussianVerbCard(pathToDb,pathToSdict)


class RussianDeck(Deck):
	name = "Russian"
	csvname = 'russian'

	cardType = None

	subdecks = []

	def __init__(self,pathToDb,pathToSdict):
		nouns = Deck()
		nouns.name = "Nouns"
		nouns.csvname = 'nouns'
		nouns.cardType = RussianSoundCard(pathToDb,pathToSdict)

		adjectives = Deck()
		adjectives.name = "Adjectives"
		adjectives.csvname = 'adjectives'
		adjectives.cardType = RussianSoundCard(pathToDb,pathToSdict)

		self.subdecks = [
			nouns,
			adjectives,
			RussianVerbsDeck(pathToDb,pathToSdict)
		]