"""Defines the different deck types for Japanese."""

# Import the default Deck object from the main proto directory.
from ...deck import Deck

from alphabets import *
from words import *

# Imports all of the card types specific to Japanese.
from cards import *


class JapaneseDeck(Deck):
    """Deck that holds all the other decks for Japanese."""

    name = "Japanese"

    # This is the base CSV name we use to hold data to be imported into Anki
    csvname = "ja"

    cardType = None

    subdecks = []

    def __init__(self, db, dictFile, furiFile):
        Deck.__init__(self)

        alphabets = AlphabetsDeck(db)

        words = WordsDeck(db, dictFile, furiFile)

        self.subdecks = [alphabets, words]
