from ...deck import Deck
from cards import *

class GermanVerbsDeck(Deck):
    name = "Verbs"
    csvname = 'verbs'
    cardType = None
    languageCode = 'de'

    def __init__(self,db):
        self.cardType = GermanVerbCard(db)


class GermanDeck(Deck):
    name = "German"
    csvname = 'de'
    cardType = None
    languageCode = 'de'

    subdecks = []

    def __init__(self,db):
        nouns = Deck()
        nouns.name = "Nouns"
        nouns.csvname = 'nouns'
        nouns.cardType = DefaultWikiSoundCard(db,'German','de')

        adjectives = Deck()
        adjectives.name = "Adjectives"
        adjectives.csvname = 'adjectives'
        adjectives.cardType = DefaultWikiSoundCard(db,'German','de')

        self.subdecks += [
            nouns,
            adjectives,
            GermanVerbsDeck(db)
        ]
