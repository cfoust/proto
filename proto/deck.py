"""The Deck class either contains subdecks or a card type. The Deck does not generate cards itself, but passes
generation calls down to its CardType (if it has one) and thus to the FieldTypes. Offers properties that control how
the deck will be studied in Anki, how frequently, etc."""
import string
import copy
import functools
import genanki

from typing import List, Optional, Generic, TypeVar

from proto.model import Model

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
        "mult": 0.0,
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
        "maxIvl": 36500,
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
        "order": 1,
    },
    # Whether or not to autoplay card sounds
    "autoplay": True,
    # Not really used for anything, but you can set this to an ISO-639-1 code so the deck can be used by addons
    "addon_foreign_language": "ru",
}

Data = TypeVar("Data")


def prefix_deck(name: str, deck: genanki.Deck) -> genanki.Deck:
    deck.name = "%s::%s" % (name, deck.name)
    return deck


class Deck(Generic[Data]):
    """
    Representation of an Anki deck which can either contain cards or subdecks.
    """

    def __init__(
        self,
        _id: int,
        name: str,
        model: Optional[Model] = None,
        data: Optional[List[Data]] = None,
        subdecks: Optional[List["Deck"]] = None,
    ) -> None:
        self.id = _id
        self.name = name
        self.model = model
        self.subdecks = subdecks or []
        self.conf = copy.deepcopy(defaultStudyConf)
        self.data = data or []

    def to_genanki(self) -> List[genanki.Deck]:
        """
        Recursively build the Deck and create input to genanki.
        """
        main = genanki.Deck(self.id, self.name,)

        return functools.reduce(
            lambda a, v: a
            + list(map(lambda b: prefix_deck(self.name, b), v.to_genanki())),
            self.subdecks,
            [main],
        )

    def build(self, path: str, media: bool = True):
        pass
