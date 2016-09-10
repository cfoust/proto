from proto.db import *
from proto.builder import *

from proto.languages.ja import JapaneseDeck

# Helps us with all of the pathing
ph = PathHelper('ja')

# The actual deck structure
jd = JapaneseDeck(sqlite(ph.db()))

# Apply Templates
applyDefaultTemplate(jd)

bd = Builder('ja', jd)

# import numpy
# raw_input("Cae is the cutest thing ever") 



# Check if we need stuff
if bd.needAnyData():

    hiriganaChars = fileLines(ph.input('hiragana.txt'))
    bd.bindDeckData('Japanese::Hiragana::Sound', hiriganaChars)
    bd.bindDeckData('Japanese::Hiragana::Stroke', hiriganaChars)

    katakanaChars = fileLines(ph.input('katakana.txt'))
    bd.bindDeckData('Japanese::Katakana::Sound', katakanaChars)
    bd.bindDeckData('Japanese::Katakana::Stroke', katakanaChars)

    radicals = fileLines(ph.input('radicals.txt'))
    bd.bindDeckData('Japanese::Radicals::Meaning', radicals)
    bd.bindDeckData('Japanese::Radicals::Stroke', radicals)

bd.build()
