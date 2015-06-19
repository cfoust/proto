from ...fields import *
from ...cards import *
from fields import *
from wikiinfo import WikiInfo

class RussianVerbCard(BasicCardType):
    name = "Russian Verb"

    fields = []

    def __init__(self,pathToDb,pathToSdict):
        self.info = WikiInfo(pathToDb,pathToSdict)
        imperfective = FieldType(True)
        imperfective.anki_name = "Imperfective"
        imperfective.order = 0

        perfective = FieldType(False)
        perfective.anki_name = "Perfective"
        perfective.order = 1

        meaning = PriorityFieldType([
            SDictField(pathToSdict),
            WiktionaryField(pathToDb,'Russian','ru'),
            RuktionaryField(pathToDb)
        ]) # A priority setup
        meaning.anki_name = "Meaning"
        meaning.order = 4
        meaning.html = "<div class='content'>%s</div>"

        audio = ForvoField(pathToDb,'ru')
        audio.anki_name = "Audio"

        imperfectiveConj = StarlingVerbField(pathToDb)
        imperfectiveConj.anki_name = 'Imperfective_Conj'
        imperfectiveConj.html = '<div style="display: none">%s</div>'

        perfectiveConj = StarlingVerbField(pathToDb)
        perfectiveConj.anki_name = 'Perfective_Conj'
        perfectiveConj.html = '<div style="display: none">%s</div>'

        imperfectiveStress = RussianVerbStressField(pathToDb,pathToSdict)
        imperfectiveStress.anki_name = 'Imperfective_Stress'
        imperfectiveStress.html = """{{#Imperfective_Stress}}
<div class='content' id = 'impf'><b>Imperfective: </b>{{Imperfective_Stress}}<br></div>
{{/Imperfective_Stress}}"""
        imperfectiveStress.order = 2

        perfectiveStress = RussianVerbStressField(pathToDb,pathToSdict)
        perfectiveStress.anki_name = 'Perfective_Stress'
        perfectiveStress.html = """{{#Perfective_Stress}}
<div class='content' id = 'pf'><b>Perfective: </b>{{Perfective_Stress}}<br></div>
{{/Perfective_Stress}}"""
        perfectiveStress.order = 3

        ctype = FieldType(False)
        ctype.anki_name = "Type"
        ctype.html = """<div class="content" style="display: none;">%s</div>"""

        self.fields = [
            imperfective,
            perfective,
            meaning,
            audio,
            imperfectiveConj,
            perfectiveConj,
            imperfectiveStress,
            perfectiveStress,
            ctype
        ]

        self.cards = []

    def generate(self,word):
        card = [None for x in range(9)]

        wordAspect = self.info.getAspect(word)
        wordPair = self.info.getAspectualPair(word)
        wordPairAspect = self.info.getAspect(wordPair)

        imperfective = None
        perfective = None
        if wordAspect == 'impf':
            imperfective = word
        else:
            perfective = word

        if wordPairAspect == 'impf':
            imperfective = wordPair
        else:
            perfective = wordPair

        if imperfective:
            try:
                imperfective = imperfective.encode('utf-8')
            except:
                pass
            card[0] = imperfective
            card[4] = self.fields[4].pull(imperfective)
            card[6] = self.fields[6].pull(imperfective)
        else:
            card[0] = ''
            card[4] = ''
            card[6] = ''

        if perfective:
            try:
                perfective = perfective.encode('utf-8')
            except:
                pass
            card[1] = perfective
            card[5] = self.fields[5].pull(perfective)
            card[7] = self.fields[7].pull(perfective)
        else:
            card[1] = ''
            card[5] = ''
            card[7] = ''

        if imperfective:
            for subfield in self.fields[2]:
                result = subfield.pull(imperfective)
                if result:
                    card[2] = result
                    break
            card[3] = self.fields[3].pull(imperfective)
            card[8] = imperfective
        elif perfective:
            for subfield in self.fields[2]:
                result = subfield.pull(perfective)
                if result:
                    card[2] = result
                    break
            card[3] = self.fields[3].pull(perfective)
            card[8] = perfective

        if not None in card:
            self.cards.append(card)
        return card

class RussianSoundCard(DefaultWikiSoundCard):
    name = 'Sound and Wiktionary'

    def __init__(self,pathToDb,pathToSdict):
        front = FieldType(True)
        front.anki_name = "Front"

        meaning = PriorityFieldType([
            SDictField(pathToSdict),
            WiktionaryField(pathToDb,'Russian','ru'),
            RuktionaryField(pathToDb)
        ]) # A priority setup
        meaning.anki_name = "Meaning"
        meaning.html = "<div class='content'>%s</div>"

        sound = ForvoField(pathToDb,'ru')
        sound.anki_name = "Audio"

        # This field has no purpose (i.e won't be displayed but here for legacy)
        type = FieldType()
        type.anki_name = "Type"
        type.html = """<div class="content" style="display: none;">%s</div>"""

        self.fields = [front,meaning,sound,type]

        self.cards = []