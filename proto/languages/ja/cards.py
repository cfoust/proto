from ...fields import *
from ...cards import *

class HiraganaCard(BasicCardType):
    name = 'Hiragana Character'

    def __init__(self,db):
        front = FieldType(True)
        front.anki_name = "Front"
        front.html = '<div class="content" style="font-size: 1200%; text-align: center;">%s</div>'

        sound = ForvoField(db, 'ja')
        sound.anki_name = "Audio"

        self.fields = [front, sound]

        self.cards = []

class KatakanaCard(BasicCardType):
    name = 'Katakana Character'

    def __init__(self,db):
        front = FieldType(True)
        front.anki_name = "Front"
        front.html = '<div class="content" style="font-size: 1200%; text-align: center;">%s</div>'

        sound = ForvoField(db, 'ja')
        sound.anki_name = "Audio"

        self.fields = [front, sound]

        self.cards = []