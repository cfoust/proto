from proto.db import *
from proto.builder import *

from proto.languages.ja import JapaneseDeck

ph = PathHelper('ja')

jd = JapaneseDeck(sqlite('proto.db'))

# Apply Templates
applyDefaultTemplate(jd)

bd = Builder('ja', jd)

# Check if we need stuff
if bd.needAnyData():

    hiriganaChars = fileLines(ph.ifile('hiragana.txt'))
    bd.bindDeckData('Japanese::Hiragana', hiriganaChars)

    katakanaChars = fileLines(ph.ifile('katakana.txt'))
    bd.bindDeckData('Japanese::Katakana', katakanaChars)

bd.build(ignoreMedia=False)
