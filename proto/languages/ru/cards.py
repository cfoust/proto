from ...fields import *
from ...cards import *
from fields import *
from wikiinfo import WikiInfo



class RussianVerbCard(BasicCardType):
    name = "Russian Verb"

    fields = []

    def __init__(self,db,pathToSdict):
        self.info = WikiInfo(db,pathToSdict)
        imperfective = FieldType(True)
        imperfective.anki_name = "Imperfective"
        imperfective.order = 0


        perfective = FieldType(False)
        perfective.anki_name = "Perfective"
        perfective.order = 1
        perfective.html = '{{^Imperfective}}<div class="content">%s</div>{{/Imperfective}}'

        enmeaning = PriorityFieldType([
            SDictField(pathToSdict),
            WiktionaryField(db,'Russian','ru')
        ]) # A priority setup
        enmeaning.anki_name = "En_Meaning"
        enmeaning.order = 4

        rumeaning = RuktionaryField(db)
        rumeaning.anki_name = "Ru_Meaning"

        Switchable('ru','en',rumeaning, enmeaning)

        audio = ForvoField(db,'ru')
        audio.anki_name = "Audio"

        imperfectiveConj = StarlingVerbField(db)
        imperfectiveConj.anki_name = 'Imperfective_Conj'
        imperfectiveConj.html = '<div style="display: none">%s</div>'

        perfectiveConj = StarlingVerbField(db)
        perfectiveConj.anki_name = 'Perfective_Conj'
        perfectiveConj.html = '<div style="display: none">%s</div>'

        imperfectiveStress = RussianVerbStressField(db,pathToSdict)
        imperfectiveStress.anki_name = 'Imperfective_Stress'
        imperfectiveStress.html = """{{#Imperfective_Stress}}
<div class='content' id = 'impf'><b>Imperfective: </b>{{Imperfective_Stress}}<br></div>
{{/Imperfective_Stress}}"""
        imperfectiveStress.order = 2

        perfectiveStress = RussianVerbStressField(db,pathToSdict)
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
            enmeaning,
            rumeaning,
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

        # Get the aspect, pair, and the pair's aspect
        wordAspect = self.info.getAspect(word)
        wordPair = self.info.getAspectualPair(word)
        wordPairAspect = self.info.getAspect(wordPair)

        imperfective = None
        perfective = None

        if wordAspect == 'both':
            wordAspect = 'impf'

        # If we have both a perfective and imperfective form
        if wordAspect == 'impf' and wordPairAspect == 'pf':
            imperfective = word
            perfective = wordPair
        elif wordAspect == 'pf' and wordPairAspect == 'impf':
            imperfective = wordPair
            perfective = word
        # If we have just an imperfective form
        elif wordAspect == 'impf':
            imperfective = word
        # If we have just a perfective form
        elif wordAspect == 'pf':
            perfective = word

        # If the imperfective form exists
        if imperfective:
            try:
                imperfective = imperfective.encode('utf-8')
            except:
                pass

            # Prioritize this as the headword
            card[0] = imperfective

            # Get the definitions based on imperfective
            card[2] = self.fields[2].pull(imperfective)
            card[3] = self.fields[3].pull(imperfective)

            # Get the sound for imperfective
            card[4] = self.fields[4].pull(imperfective)

            # Get the conjugation for imperfective
            card[5] = self.fields[5].pull(imperfective)

            # Get the stress for imperfective
            card[7] = self.fields[7].pull(imperfective)

        # If the perfective form exists
        if perfective:
            try:
                perfective = perfective.encode('utf-8')
            except:
                pass

            # Set the second field as the perfective form
            card[1] = perfective

            # Get the perfective conjugation
            card[6] = self.fields[6].pull(perfective)

            # Get the stress for perfective
            card[8] = self.fields[8].pull(perfective)

        # When we just have a perfective verb
        if perfective and not imperfective:
            # Get the definitions based on perfective
            card[2] = self.fields[2].pull(perfective)
            card[3] = self.fields[3].pull(perfective)

            # Get the sound for imperfective
            card[4] = self.fields[4].pull(perfective)

        if imperfective and not perfective:
            # Make these not None, just empty
            card[1] = ''
            card[6] = ''
            card[8] = ''

        if not (card[0] == None and card[1] == None) and not card[2] == None:
            self.cards.append(card)

        return card

class RussianSoundCard(DefaultWikiSoundCard):
    name = 'Sound and Wiktionary'

    def __init__(self,db,pathToSdict):
        front = FieldType(True)
        front.anki_name = "Front"

        enmeaning = PriorityFieldType([
            SDictField(pathToSdict),
            WiktionaryField(db,'Russian','ru')
        ]) # A priority setup
        enmeaning.anki_name = "En_Meaning"

        rumeaning = RuktionaryField(db)
        rumeaning.anki_name = "Ru_Meaning"

        Switchable('ru','en',rumeaning, enmeaning)

        sound = ForvoField(db,'ru')
        sound.anki_name = "Audio"

        # This field has no purpose (i.e won't be displayed but here for legacy)
        type = FieldType()
        type.anki_name = "Type"
        type.html = """<div class="content" style="display: none;">%s</div>"""

        self.fields = [front,enmeaning,rumeaning,sound,type]

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