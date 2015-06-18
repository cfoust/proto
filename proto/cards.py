from fields import *
import copy, string

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

	# For apkg generation
	mid = 0

	def __init__(self):
		# The default card front that shows the word
		front = FieldType(True)
		front.name = "FrontSide"
		self.fields += front

		self.cards = []

	def generate(self,word):
		card = []
		for field in self.fields:
			result = field.pull(word)
			card.append(result)
		if not None in card:
			self.cards.append(card)
		return card

	def fillIn(self,word,card):
		if not len(card) == len(self.fields):
			raise Exception('Invalid number of fields.')

		for i,field in enumerate(card):
			if not field:
				card[i] = self.fields[i].pull(word)

		if not None in card:
			self.cards.append(card)
		return card

	def _sortFields(self):

		numericFields = sorted([f for f in self.fields if f.order != -1], key=lambda f: f.order)
		normalFields = [f for f in self.fields if f.order == -1]
		return numericFields + normalFields

	def front(self):

		front = "<script>%s</script>" % self.js()

		front += self._fheader

		for field in self._sortFields():
			fieldHtml = field.html.replace('%s','{{%s}}' % field.anki_name)
			if field.front:
				front += fieldHtml

		front += self._ffooter

		return front

	def back(self):
		back = "<script>%s</script>" % self.js()

		wordField = self.fields[0]
		wordHtml = wordField.html.replace('%s','{{%s}}' % wordField.anki_name)
		back += wordHtml

		back += self._bheader

		for i,field in enumerate(self._sortFields()):
			fieldHtml = field.html.replace('%s','{{%s}}' % field.anki_name)
			if not field.front:
				back += fieldHtml

		back += self._bfooter

		return back

	def css(self):
		return self._css + '\n'.join([field.css for field in self.fields])

	def js(self):
		return self._js + '\n'.join([field.js for field in self.fields])

	def shortName(self):
		return string.replace(self.name.lower(),' ','-')

class DefaultWikiSoundCard(BasicCardType):
	name = "Sound and Wiktionary"

	mid = 1376518451077

	def __init__(self,pathToDb,languageFullName,languageCode):
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