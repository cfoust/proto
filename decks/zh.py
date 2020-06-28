from proto.db import sqlite
from proto.butils import fileLines
from proto.builder import PathHelper, Builder

from proto.languages.zh.deck import MandarinDeck

# Helps us with all of the pathing
ph = PathHelper("zh")

# The actual deck structure
deck = MandarinDeck(sqlite(ph.db()))

# Apply Templates
# applyDefaultTemplate(jd, css='ja/style.css', js='ja/ja.js', header=None, footer=None)

builder = Builder("zh", deck)


def get_word_data(filename):
    lines = fileLines(ph.input(filename))
    return list(map(lambda a: a.split("\t"), lines))


# Check if we need stuff
if builder.needAnyData():
    words = {
        "verb": get_word_data("verbs")[:2000],
        "noun": get_word_data("nouns")[:4000],
        "adj": get_word_data("adjectives")[:4000],
    }

    builder.bindDeckData("Mandarin::Nouns", words["noun"])
    builder.bindDeckData("Mandarin::Adjectives", words["adj"])
    builder.bindDeckData("Mandarin::Verbs", words["verb"])

builder.build()
