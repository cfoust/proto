from ...deck import Deck
from cards import *

class GermanVerbsDeck(Deck):
    name = "Verbs"
    csvname = 'verbs'
    cardType = None
    languageCode = 'de'

    def __init__(self,pathToDb):
        self.cardType = GermanVerbCard(pathToDb)


class GermanDeck(Deck):
    name = "German"
    csvname = 'de'
    cardType = None
    languageCode = 'de'

    subdecks = []

    def __init__(self,pathToDb):
        nouns = Deck()
        nouns.name = "Nouns"
        nouns.csvname = 'nouns'
        nouns.cardType = DefaultWikiSoundCard(pathToDb,'German','de')

        adjectives = Deck()
        adjectives.name = "Adjectives"
        adjectives.csvname = 'adjectives'
        adjectives.cardType = DefaultWikiSoundCard(pathToDb,'German','de')

        self.subdecks += [
            nouns,
            adjectives,
            GermanVerbsDeck(pathToDb)
        ]
