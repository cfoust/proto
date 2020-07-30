"""The Deck class either contains subdecks or a card type. The Deck does not generate cards itself, but passes
generation calls down to its CardType (if it has one) and thus to the FieldTypes. Offers properties that control how
the deck will be studied in Anki, how frequently, etc."""
import string
import copy
import functools
import genanki
import tempfile
import zipfile
import time
import os
import sqlite3
import json

from typing import List, Optional, Generic, TypeVar, Tuple

from proto.field import Media
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

    def to_genanki(self) -> List[Tuple[genanki.Deck, List[Media]]]:
        """
        Recursively build the Deck and create input to genanki.
        """
        main = genanki.Deck(self.id, self.name,)

        model = self.model
        media: List[Media] = []
        if model is not None:
            notes, files = model.to_genanki(self.data)
            media = media + files

        return functools.reduce(
            lambda a, v: a
            + list(map(lambda b: (prefix_deck(self.name, b[0]), b[1]), v.to_genanki())),
            self.subdecks,
            [(main, media)],
        )

    def build(self, file: str, include_media: bool = True):
        """
        This partially reimplements the apkg export from genanki because we
        don't want to keep our files on the disk itself, rather they come from
        sqlite.
        """
        dbfile, dbfilename = tempfile.mkstemp()
        os.close(dbfile)

        conn = sqlite3.connect(dbfilename)
        cursor = conn.cursor()

        now_ts = int(time.time())

        results = self.to_genanki()
        decks: List[genanki.Deck] = []
        media: List[Media] = []

        for deck, files in results:
            decks.append(deck)
            media = media + files

        for deck in decks:
            deck.write_to_db(cursor, now_ts)

        conn.commit()
        conn.close()

        with zipfile.ZipFile(file, 'w') as outzip:
            outzip.write(dbfilename, 'collection.anki2')

            media_file_idx = dict(enumerate(media))
            media_json = {idx: obj["filename"] for idx, obj in media_file_idx.items()}
            outzip.writestr('media', json.dumps(media_json))

            for idx, obj in media_file_idx.items():
                outzip.writestr(str(idx), obj["data"])
