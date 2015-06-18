import string

"""Just establishes the framework that the specific decks will inherit from."""


defaultStudyConf = {
        "replayq": True,
        "lapse": {
            "leechFails": 8,
            "minInt": 1,
            "delays": [3],
            "leechAction": 0,
            "mult": 0.0
        },
        "rev": {
            "perDay": 500,
            "ivlFct": 0.5,
            "fuzz": 0.05,
            "ease4": 1.3,
            "bury": True,
            "minSpace": 1,
            "maxIvl": 36500
        },
        "timer": 0,
        "dyn": False,
        "maxTaken": 60,
        "usn": 0,
        "new": {
            "separate": True,
            "delays": [1, 3, 5, 8, 10, 15],
            "perDay": 5,
            "ints": [1, 1, 7],
            "initialFactor": 2500,
            "bury": True,
            "order": 1
        },
        "autoplay": True,
        "addon_foreign_language": "ru"
    }

class Deck:
	name = "Default"
	subdecks = []
	cardType = None
	csvname = 'default'
	languageCode = None
	conf = defaultStudyConf
	perDay = None

	# Generates a card for all the card types in the deck, but not sub decks.
	def makeCard(self,word):
		if not self.cardType:
			raise Exception('Deck has no card type.')
		return self.cardType.generate(word)

	def subDeckByName(self,name):
		for deck in self.subdecks:
			if deck.name == name:
				return deck

	def shortName(self):
		return string.replace(self.name.lower(),' ','-')