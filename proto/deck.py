"""The Deck class either contains subdecks or a card type. The Deck does not generate cards itself, but passes
generation calls down to its CardType (if it has one) and thus to the FieldTypes. Offers properties that control how
the deck will be studied in Anki, how frequently, etc."""
import string

# This is directly taken from Anki's database.
defaultStudyConf = {
        "replayq": True,

        # Options for what happens when the user forgets a card.
        "lapse": {
            # Maximum allowed failures before card is suspended.
            "leechFails": 8,

            "minInt": 1,

            # Try again in 3 minutes on failure
            "delays": [3],

            "leechAction": 0,
            "mult": 0.0
        },

        # Options for reviews
        "rev": {
            # Maximum reviews allowed per day
            "perDay": 500,

            "ivlFct": 0.5,
            "fuzz": 0.05,

            # Current difficulty is multiplied by this on success
            "ease4": 1.3,

            "bury": True,
            "minSpace": 1,
            "maxIvl": 36500
        },
        "timer": 0,
        "dyn": False,
        "maxTaken": 60,
        "usn": 0,

        # Options for new cards
        "new": {
            "separate": True,

            # Intervals for each new card. Value is in minutes.
            "delays": [1, 3, 5, 8, 10, 15],

            # New cards per day.
            "perDay": 5,

            "ints": [1, 1, 7],

            # Initial difficulty
            "initialFactor": 2500,

            "bury": True,
            "order": 1
        },

        # Whether or not to autoplay card sounds
        "autoplay": True,

        # Not really used for anything, but you can set this to an ISO-639-1 code so the deck can be used by addons
        "addon_foreign_language": "ru"
    }

class Deck:
    """ Representation of an Anki deck which can either contain cards or sub-decks, but never both. Stores a card
    type that is used to generate a card."""

    # Name which is used by Anki
    name = "Default"

    # Any subdecks we might have
    subdecks = []

    # The card type. See documentation for BasicCardType.
    cardType = None

    # Used by the builders to generate a csv for this deck. Should be a valid file name.
    csvname = 'default'

    # ISO-639-1 Code Corresponding to the language this deck builds for. Optional.
    languageCode = None

    # Configuration for this deck. See above default config.
    conf = defaultStudyConf

    # Instead of changing a part of the config, this optional variable lets you choose how many new cards will show
    # in a day.
    perDay = None

    def makeCard(self, word):
        """Generates a card for the card type.
        Returns: Array set of fields that correspond to the fields of the card."""

        if not self.cardType:
            raise Exception('Deck has no card type.')

        return self.cardType.generate(word)

    def subDeckByName(self,name):
        """Gets a subdeck by name. A subdeck has all the properties of a normal deck.
        Returns: the subdeck Deck instance."""

        for deck in self.subdecks:
            if deck.name == name:
                return deck

    def shortName(self):
        """Returns this deck's short name as a string. The short name is just the Anki name but, well, shorter."""
        return string.replace(self.name.lower(), ' ', '-')
