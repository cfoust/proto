from proto.db import *
from proto.builder import *

from decks.ja.jmdict import JMDictGetter, JMReadingGetter

# Helps us with all of the pathing
ph = PathHelper("ja")

# The actual deck structure
jd = JapaneseDeck(sqlite(ph.db()), ph.input("JMdict_e"))

WordCard = proto.Model(
    1527532200,
    "ja-word",
    guid=lambda data: data[0],
    fields=[
        Field("Headword", lambda data: data[0],),
        Field("Reading", JMReadingGetter(ph.input("JmdictFurigana.txt"))),
        Field("Definition", JMDictGetter(ph.input("JMdict_e"))),
        # The part of speech
        Field("POS", lambda data: data[-1],),
    ],
    templates=[{"name": "Card 1", "front": "", "back": "",}],
)

words = {
    "verb": get_file_lines(ph.input("verb-base.csv")),
    "noun": get_file_lines(ph.input("noun-base.csv")),
    "adj": get_file_lines(ph.input("adj-base.csv")),
}

deck = Deck(
    # The name of the deck
    "Japanese",
    [Deck("Nouns", Model, words["noun"],)],
)

deck.build()
