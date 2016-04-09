from ...fields import *
from ...cards import *
from fields import *
from wikiinfo import WikiInfo

dualMeaningHTML = """
<div id='ru-mean' style='display:none'>{{Ru_Meaning}}</div>
<div id='en-mean' style='display:none'>{{En_Meaning}}</div>

<button id="left-button" class="content-button left-button">ru</button>
<button id="right-button"  class="content-button right-button">en</button>
<div class="top-cut content" id='asd'>none</div>
"""

dualMeaningJS = """
var left = document.getElementById('left-button');

var selectLeft = function() {
    var text = document.getElementById('ru-mean').innerHTML;
    var leftClasses = "content-button left-button content-button-selected";
    var rightClasses = "content-button right-button";

    document.getElementById('asd').innerHTML = text;
    document.getElementById('left-button').className = leftClasses;
    document.getElementById('right-button').className = rightClasses;
}

left.onclick = selectLeft;
left.touchstart = selectLeft;

var right = document.getElementById('right-button');

var selectRight = function() {
    var text = document.getElementById('en-mean').innerHTML;
    var rightClasses = "content-button right-button content-button-selected";
    var leftClasses = "content-button left-button";

    document.getElementById('asd').innerHTML = text;
    document.getElementById('left-button').className = leftClasses;
    document.getElementById('right-button').className = rightClasses;
}

right.onclick = selectRight;
right.touchstart = selectRight;

selectLeft();
"""

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
        perfective.html = '{{^Imperfective}}<div class="content">%s</div>{{/Imperfective}}'

        enmeaning = PriorityFieldType([
            SDictField(pathToSdict),
            WiktionaryField(pathToDb,'Russian','ru')
        ]) # A priority setup
        enmeaning.anki_name = "En_Meaning"
        enmeaning.order = 4
        enmeaning.html = ""

        rumeaning = RuktionaryField(pathToDb)
        rumeaning.anki_name = "Ru_Meaning"
        rumeaning.html = dualMeaningHTML
        rumeaning.js = dualMeaningJS

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

        # If we have both a perfective and imperfective form
        if wordAspect == 'impf' and wordPairAspect == 'pf':
            imperfective = word
            perfective = wordPair
        # If we have just an imperfective form
        elif wordAspect == 'impf' and (not wordPairAspect or not wordPair):
            imperfective = word
        # If we have just a perfective form
        elif wordAspect == 'pf' and (not wordPairAspect or not wordPair):
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

        if not None in card[0:2] + card[4:] and not (card[2] == None and card[3] == None):
            self.cards.append(card)

        return card

class RussianSoundCard(DefaultWikiSoundCard):
    name = 'Sound and Wiktionary'

    def __init__(self,pathToDb,pathToSdict):
        front = FieldType(True)
        front.anki_name = "Front"

        enmeaning = PriorityFieldType([
            SDictField(pathToSdict),
            WiktionaryField(pathToDb,'Russian','ru')
        ]) # A priority setup
        enmeaning.anki_name = "En_Meaning"
        enmeaning.html = ""

        rumeaning = RuktionaryField(pathToDb)
        rumeaning.anki_name = "Ru_Meaning"
        rumeaning.html = dualMeaningHTML
        rumeaning.js = dualMeaningJS

        sound = ForvoField(pathToDb,'ru')
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