from proto.db import *
from proto.builder import *

from proto.languages.ja import JapaneseDeck

# Helps us with all of the pathing
ph = PathHelper('ja')

# The actual deck structure
jd = JapaneseDeck(sqlite(ph.db()), 
                  ph.input('JMdict_e'), 
                  ph.input('JmdictFurigana.txt'))

# Apply Templates
applyDefaultTemplate(jd, css='ja/style.css', js='ja/ja.js', header=None, footer=None)

bd = Builder('ja', jd)

# Check if we need stuff
if bd.needAnyData():

    hiriganaChars = fileLines(ph.input('hiragana.txt'))
    bd.bindDeckData('Japanese::Alphabets::Hiragana::Sound', hiriganaChars)
    bd.bindDeckData('Japanese::Alphabets::Hiragana::Stroke', hiriganaChars)

    katakanaChars = fileLines(ph.input('katakana.txt'))
    bd.bindDeckData('Japanese::Alphabets::Katakana::Sound', katakanaChars)
    bd.bindDeckData('Japanese::Alphabets::Katakana::Stroke', katakanaChars)

    radicals = fileLines(ph.input('radicals.txt'))
    bd.bindDeckData('Japanese::Alphabets::Radicals::Meaning', radicals)
    bd.bindDeckData('Japanese::Alphabets::Radicals::Stroke', radicals)

    words = fileLines(ph.input('base_aggregates_fixed.txt'))
    nouns = []
    for line in words:
        parts = line.split('\t')

        if parts[2] == 'noun':
            nouns.append(parts[1])

    nouns.reverse()

    bd.bindDeckData('Japanese::Words::Nouns', nouns)

bd.build()
