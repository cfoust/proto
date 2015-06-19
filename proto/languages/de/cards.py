from ...fields import *
from ...cards import *
from fields import *

class GermanVerbCard(BasicCardType):
    name = "German Verb"

    fields = []

    def __init__(self,pathToDb):

        word = FieldType(True)
        word.anki_name = "Word"

        meaning = WiktionaryField(pathToDb,'German','de')
        meaning.anki_name = "Meaning"

        sound = ForvoField(pathToDb,'de')
        sound.anki_name = "Sound"

        conjugation = GermanVerbixField(pathToDb)
        conjugation.anki_name = "Conjugation"

        self.fields = [word,meaning,sound,conjugation]
