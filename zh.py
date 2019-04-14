from proto.db import *
from proto.builder import *

from proto.languages.zh import MandarinDeck

# Helps us with all of the pathing
ph = PathHelper('js')

# The actual deck structure
deck = MandarinDeck(sqlite(ph.db()))

# Apply Templates
# applyDefaultTemplate(jd, css='ja/style.css', js='ja/ja.js', header=None, footer=None)

builder = Builder('zh', deck)

# Check if we need stuff
if builder.needAnyData():
    words = {
        'verb': fileLines(ph.input('verbs')),
        'noun': fileLines(ph.input('nouns')),
        'adj': fileLines(ph.input('adjectives'))
    }

    print len(words['noun'])
    print len(words['verb'])
    print len(words['adj'])

    builder.bindDeckData('Mandarin::Nouns', words['noun'])
    builder.bindDeckData('Mandarin::Adjectives', words['adj'])
    builder.bindDeckData('Mandarin::Verbs', words['verb'])

builder.build()
