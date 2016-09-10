"""Defines the different deck types for Japanese."""

# Import the default Deck object from the main proto directory.
from ...deck import Deck

# Imports all of the card types specific to Japanese.
from cards import *

class JapaneseDeck(Deck):
    """Deck that holds all the other decks for Japanese."""

    name = "Japanese"

    # This is the base CSV name we use to hold data to be imported into Anki
    csvname = 'ja'

    cardType = None

    subdecks = []

    def __init__(self, db):
        Deck.__init__(self)


        # Creates the main hiragana deck
        hiragana = Deck()
        hiragana.name = "Hiragana"
        hiragana.csvname = 'hiragana'
        hiragana.cardType = None
        hiragana.conf["rev"]["ivlFct"] = 0.3
        hiragana.conf["rev"]["ease4"] = 1.1

        generalConf = hiragana.conf

        # Makes its symbol to sound deck
        hiraganaSymbolToSound = Deck()
        hiraganaSymbolToSound.name = "Sound"
        hiraganaSymbolToSound.csvname = 'symbol-to-sound'
        hiraganaSymbolToSound.cardType = SymbolToSoundCard(db)
        hiraganaSymbolToSound.conf = generalConf

        hiraganaSoundToStroke = Deck()
        hiraganaSoundToStroke.name = "Stroke"
        hiraganaSoundToStroke.csvname = 'sound-to-stroke'
        hiraganaSoundToStroke.cardType = SoundToStrokeCard(db)
        hiraganaSoundToStroke.conf = generalConf

        hiragana.subdecks = [
            hiraganaSymbolToSound,
            hiraganaSoundToStroke
        ]

        katakana = Deck()
        katakana.name = "Katakana"
        katakana.csvname = 'katakana'
        katakana.cardType = None
        katakana.conf = generalConf

        # Makes its symbol to sound deck
        katakanaSymbolToSound = Deck()
        katakanaSymbolToSound.name = "Sound"
        katakanaSymbolToSound.csvname = 'symbol-to-sound'
        katakanaSymbolToSound.cardType = SymbolToSoundCard(db)
        katakanaSymbolToSound.conf = generalConf

        katakanaSoundToStroke = Deck()
        katakanaSoundToStroke.name = "Stroke"
        katakanaSoundToStroke.csvname = 'sound-to-stroke'
        katakanaSoundToStroke.cardType = SoundToStrokeCard(db)
        katakanaSoundToStroke.conf = generalConf

        katakana.subdecks = [
            katakanaSymbolToSound,
            katakanaSoundToStroke
        ]

        radicals = Deck()
        radicals.name = "Radicals"
        radicals.csvname = 'radicals'
        radicals.cardType = None
        radicals.conf = generalConf

        radicalMeaning = Deck()
        radicalMeaning.name = "Meaning"
        radicalMeaning.csvname = 'meaning'
        radicalMeaning.cardType = RadicalInfo()
        radicalMeaning.conf = generalConf

        radicalStroke = Deck()
        radicalStroke.name = "Stroke"
        radicalStroke.csvname = 'stroke'
        radicalStroke.cardType = RadicalStroke()
        radicalStroke.conf = generalConf

        radicals.subdecks = [
            radicalMeaning,
            radicalStroke
        ]

        self.subdecks = [
            hiragana,
            katakana,
            radicals
        ]