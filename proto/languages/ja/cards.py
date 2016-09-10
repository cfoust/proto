from ...fields import *
from ...cards import *

class SymbolToSoundCard(BasicCardType):
    name = 'ja-character-to-sound'

    def __init__(self,db):
        front = FieldType(True)
        front.anki_name = "Front"
        front.html = '<div class="content" style="font-size: 1200%; text-align: center;">%s</div>'

        sound = ForvoField(db, 'ja')
        sound.anki_name = "Audio"

        self.fields = [front, sound]

        self.cards = []

class SoundToStrokeCard(BasicCardType):
    name = 'ja-sound-to-stroke'

    def __init__(self,db):
        sound = ForvoField(db, 'ja')
        sound.front = True
        sound.anki_name = "Audio"



        # The stroke order goes on the back
        stroke = FieldType()
        stroke.anki_name = "Stroke"
        stroke.html = '<div class="content" style="font-size: 1200%; text-align: center; font-family: strokefont;">%s</div>'
        stroke.css = """@font-face {
  font-family: 'strokefont';
  src: url('kanji.ttf')  format('truetype');
}"""

        self.fields = [sound, stroke]

        self.cards = []


class RadicalInfo(BasicCardType):
    name = 'ja-radical-meaning'

    def __init__(self):
        front = FieldType(True)
        front.anki_name = "Front"
        front.html = '<div class="content" style="font-size: 1200%; text-align: center;">%s</div>'

        meaning = FieldType()
        meaning.anki_name = "Meaning"

        name = FieldType()
        name.anki_name = "Name"
        name.html = """{{#Name}}
<div class="content center">%s</div>
{{/Name}}"""

        examples = FieldType()
        examples.anki_name = "Examples"

        self.fields = [
            front,
            meaning,
            name,
            examples
        ]

        self.cards = []

    def generate(self,word):
        card = ['' for x in range(4)]

        parts = word.split("\t")

        card[0] = parts[0]
        card[1] = parts[3]
        card[2] = parts[2]
        card[3] = parts[-1]

        self.cards.append(card)

class RadicalStroke(BasicCardType):
    name = 'ja-radical-stroke'

    def __init__(self):
        radical = FieldType(True)
        radical.anki_name = "Character"
        radical.html = '<div class="content" style="font-size: 1200%; text-align: center;">%s</div>'

        # The stroke order goes on the back
        stroke = FieldType()
        stroke.anki_name = "Stroke"
        stroke.html = '<div class="content" style="font-size: 1200%; text-align: center; font-family: strokefont;">%s</div>'
        stroke.css = """@font-face {
  font-family: 'strokefont';
  src: url('kanji.ttf')  format('truetype');
}"""

        self.fields = [radical, stroke]

        self.cards = []

    def generate(self,word):
        card = ['' for x in range(2)]

        parts = word.split("\t")

        card[0] = parts[0]
        card[1] = parts[0]

        self.cards.append(card)