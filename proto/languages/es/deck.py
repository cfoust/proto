"""Defines the different deck types for Spanish."""

# Import the default Deck object from the main proto directory.
from ...deck import Deck

# Imports all of the card types specific to Spanish.
from cards import *


class SpanishVerbsDeck(Deck):
    """Spanish verb decks behave differently from normal decks, so we have
    a specific deck type for them."""

    name = "Verbs"
    csvname = 'verbs'
    cardType = None

    def __init__(self, db, pathToSdict):
        self.cardType = SpanishVerbCard(db,pathToSdict)


class SpanishDeck(Deck):
    """Deck that holds all the other decks for Spanish."""

    name = "Spanish"

    # This is the base CSV name we use to hold data to be imported into Anki
    csvname = 'es'

    cardType = None

    subdecks = []

    def __init__(self, db, pathToSdict):
        # Creates the nouns deck
        nouns = Deck()
        nouns.name = "Nouns"
        """ The csvname here is a short (and lowercase) name that we use to 
            generate CSVs."""
        nouns.csvname = 'nouns'
        nouns.cardType = RussianSoundCard(db,pathToSdict)

        # Creates the adjectives deck
        adjectives = Deck()
        adjectives.name = "Adjectives"
        adjectives.csvname = 'adjectives'
        adjectives.cardType = RussianSoundCard(db,pathToSdict)

        self.subdecks = [
            nouns,
            adjectives,
            SpanishVerbsDeck(db,pathToSdict)
        ]