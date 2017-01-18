"""Defines and implements the card types. Card Types are just containers of FieldTypes with some extra properties
that we need to generate a valid deck for Anki. """

from .fields import *
import string

class BasicCardType:
    # Card type as it shows up in Anki
    name = "Default Card Type"

    # CSS for this card
    _css = ""

    # JS for this card
    _js = ""

    # Front HTML Header
    _fheader = ""
    # Front HTML Footer
    _ffooter = ""

    # Back HTML Header
    _bheader = ""
    # Back HTML Footer
    _bfooter = ""

    # Fields for this card type
    fields = []

    # Holds the generated cards
    cards = []

    # Corresponds to a modelid in the Anki database. A modelid is just an integer referring to a certain "model",
    # which is just a template for a card. In other words, we can use this to not overwrite previously imported
    # models during our import, or just update a pre-existing model.
    mid = 0

    def __init__(self):
        # The default card front that shows the word
        front = FieldType(True)
        front.name = "FrontSide"
        self.fields += front

        self.cards = []

    def generate(self, word):
        """Generates a card for the given word. The word string is passed into each field with no other parameters,
        and the result returned by each field is appended to the card's array. If generation is successful for every
        field, the card's array is appended to this cardType instance's list of cards.
        Returns: The resulting card array, even if it has a None value in it."""

        card = []

        # Creates the card's array using generated fields.
        for field in self.fields:
            result = field.pull(word)
            card.append(result)

        # Ensures that no field returned None.
        if not None in card:
            self.cards.append(card)

        return card

    def fillIn(self, word, card):
        """This method takes a headword and the headword's card array and fills in any values that are None. This is useful
        when you want to add a field to a cardType but don't want to regenerate all the other fields. If the resultant
        filled-in card array has no Nones, it is also appended to this card type instance's list of cards.

        The card array that you pass in should have a "None" inserted at the same index the new field was inserted.

        Returns: The resulting card array, even if it has a None value in it."""

        # Ensures we have the same number of fields.
        if not len(card) == len(self.fields):
            raise Exception('Invalid number of fields.')

        for i, field in enumerate(card):
            if not field:
                card[i] = self.fields[i].pull(word)

        if not None in card:
            self.cards.append(card)

        return card

    def _sortFields(self):
        """Returns a sorted list of fields. Fields can have order property that determine their position on the
        card itself, but are unrelated to the order they appear in the CardType's list of fields."""

        # All the fields that have the order property defined get precedence. They are sorted in ascending order.
        numericFields = sorted([f for f in self.fields if f.order != -1], key=lambda f: f.order)

        # The rest are filtered out and appended at the end.
        normalFields = [f for f in self.fields if f.order == -1]

        return numericFields + normalFields

    def front(self):
        """Gets the html for the front of the card. This includes building all of the fields' html, respecting
        field order and combining it all together. """

        # Holds all of the scripts.
        front = "<script>%s</script>" % self.js()

        # Adds the front header, which is just an html string.
        front += self._fheader

        # Appends all of the fields.
        for field in self._sortFields():
            fieldHtml = field.html.replace('%s','{{%s}}' % field.anki_name)
            if field.front:
                front += fieldHtml

        # Appends the footer, which is also just an html string.
        front += self._ffooter

        return front

    def back(self):
        """Generates the html for the back of the card. See front() for more information."""

        back = "<script>%s</script>" % self.js()

        # Puts the word at the top of the back.
        wordField = self.fields[0]
        wordHtml = wordField.html.replace('%s','{{%s}}' % wordField.anki_name)
        back += wordHtml

        # Appends the back header.
        back += self._bheader

        # Appends all the fields' html.
        for i,field in enumerate(self._sortFields()):
            fieldHtml = field.html.replace('%s','{{%s}}' % field.anki_name)
            if not field.front:
                back += fieldHtml

        # Appends the back footer.
        back += self._bfooter

        return back

    def css(self):
        """Returns the combined CSS needed by each field."""
        return self._css + '\n'.join([field.css for field in self.fields])

    def js(self):
        """Returns the combined JavaScript needed by each field."""
        return self._js + '\n'.join([field.js for field in self.fields])

    def shortName(self):
        """Gets this CardType's shortname."""
        return string.replace(self.name.lower(),' ','-')

class DefaultWikiSoundCard(BasicCardType):
    """This card takes a headword and gets its definition from English Wiktionary and its sound from Forvo."""
    name = "Sound and Wiktionary"

    # Just our static model ID we use for this card type
    mid = 1376518451077

    def __init__(self,pathToDb,languageFullName,languageCode):
        """Creates an instance of DefaultWikiSoundCard.

        pathToDb is the path to a sqlite database where cacheable information will be stored.
        languageFullName is the full English name of the target language.
        languageCode is the ISO-639-1 code for the target language. Eg: en, es, ru"""
        front = FieldType(True)
        front.anki_name = "Front"

        back = WiktionaryField(pathToDb,languageFullName,languageCode)
        back.anki_name = "Back"
        back.html = """<div class="content"\>%s</div>"""

        sound = ForvoField(pathToDb,languageCode)
        sound.anki_name = "Audio"

        # This field has no purpose (i.e won't be displayed but here for legacy)
        type = FieldType()
        type.anki_name = "Type"
        type.html = """<div class="content" style="display: none;">%s</div>"""

        self.fields = [front,back,sound,type]