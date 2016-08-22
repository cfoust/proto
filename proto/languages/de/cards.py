from ...fields import *
from ...cards import *
from fields import *

class GermanVerbCard(BasicCardType):
    name = "German Verb"

    fields = []

    def __init__(self,db):

        word = FieldType(True)
        word.anki_name = "Word"

        meaning = WiktionaryField(db,'German','de')
        meaning.anki_name = "Meaning"

        sound = ForvoField(db,'de')
        sound.anki_name = "Sound"

        conjugation = GermanVerbixField(db)
        conjugation.anki_name = "Conjugation"

        self.fields = [word,meaning,sound,conjugation]
