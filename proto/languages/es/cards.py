from ...fields import *
from ...cards import *


class SpanishSoundCard(DefaultWikiSoundCard):
    name = "Spanish Basic"

    def __init__(self, db, pathToSdict):
        front = FieldType(True)
        front.anki_name = "Front"

        enmeaning = PriorityFieldType(
            [SDictField(pathToSdict), WiktionaryField(db, "Spanish", "es")]
        )  # A priority setup
        enmeaning.anki_name = "En_Meaning"

        rumeaning = RuktionaryField(db)
        rumeaning.anki_name = "Ru_Meaning"

        Switchable("ru", "en", rumeaning, enmeaning)

        sound = ForvoField(db, "ru")
        sound.anki_name = "Audio"

        # This field has no purpose (i.e won't be displayed but here for legacy)
        type = FieldType()
        type.anki_name = "Type"
        type.html = """<div class="content" style="display: none;">%s</div>"""

        self.fields = [front, enmeaning, rumeaning, sound, type]

        self.cards = []

    def generate(self, word):

        card = []

        # Creates the card's array using generated fields.
        for field in self.fields:
            result = field.pull(word)
            card.append(result)

        # Ensures that no field returned None.
        if not (card[1] == None and card[2] == None):
            self.cards.append(card)

        return card
