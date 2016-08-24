"""Defines the different deck types for Japanese."""

# Import the default Deck object from the main proto directory.
from ...deck import Deck

# Imports all of the card types specific to Japanese.
from cards import *

class JapaneseDeck(Deck):
    """Deck that holds all the other decks for Japanese."""

    name = "Japanese"

    # This is the base CSV name we use to hold data to be imported into Anki
    csvname = 'jp'

    cardType = None

    subdecks = []

    def __init__(self, db):
        Deck.__init__(self)

        # Creates the hiragana deck
        hiragana = Deck()
        hiragana.name = "Hiragana"
        """ The csvname here is a short (and lowercase) name that we use to 
            generate CSVs."""
        hiragana.csvname = 'hiragana'
        hiragana.cardType = HiraganaCard(db)
        hiragana.conf["rev"]["ivlFct"] = 0.3
        hiragana.conf["rev"]["ease4"] = 1.1

        # Creates the katakana deck
        katakana = Deck()
        katakana.name = "Katakana"
        """ The csvname here is a short (and lowercase) name that we use to 
            generate CSVs."""
        katakana.csvname = 'katakana'
        katakana.cardType = KatakanaCard(db)
        katakana.conf["rev"]["ivlFct"] = 0.3
        katakana.conf["rev"]["ease4"] = 1.1


        self.subdecks = [
            hiragana,
            katakana
        ]