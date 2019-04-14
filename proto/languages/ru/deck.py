"""Defines the different deck types for Russian."""

# Import the default Deck object from the main proto directory.
from ...deck import Deck

# Imports all of the card types specific to Russian.
from cards import *


class RussianVerbsDeck(Deck):
    """Russian verb decks behave very differently to normal decks, so we have
    a specific deck type for them."""

    name = "Verbs"
    csvname = 'verbs'
    cardType = None

    def __init__(self,db,pathToSdict):
        self.cardType = RussianVerbCard(db,pathToSdict)


class RussianDeck(Deck):
    """Deck that holds all the other decks for Russian."""

    name = "Russian"

    # This is the base CSV name we use to hold data to be imported into Anki
    csvname = 'ru'

    cardType = None

    subdecks = []

    def __init__(self,db,pathToSdict):
        Deck.__init__(self)
        
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
            # Since the verbs deck has an implementation, we inline that
            RussianVerbsDeck(db,pathToSdict)
        ]