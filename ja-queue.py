from proto.db import *
from proto.builder import *

from proto.languages.ja import *

# Helps us with all of the pathing
ph = PathHelper('ja')

# The actual deck structure
jd = WordsDeck(sqlite(ph.db()), 
                  ph.input('JMdict_e'), 
                  ph.input('JmdictFurigana.txt'))

# Apply Templates
applyDefaultTemplate(jd, css='ja/style.css', js='ja/ja.js', header=None, footer=None)

bd = Builder('ja', jd)

words = fileLines(ph.input('input.csv'))
bd.bindDeckData('Words::Nouns', words)

bd.build()
