"""
Class that allows you to grab cards, media, and other stuff from existing Anki
.apkg files.
"""

import functools
import zipfile
import sqlite3
import json
import tempfile
import os
import re

from typing import List, Dict, Optional, Generic, TypeVar, Tuple, Callable, Any

from proto.field import FieldFunction, Data, FieldResult

# guid, fields
NoteResult = Tuple[str, List[str]]

SOUND_REGEX = re.compile("\[sound:(.+)\]")

FIELD_SPLIT = "\x1f"


def split_fields(target: str) -> List[str]:
    return target.split(FIELD_SPLIT)


def normalize_media(file: str) -> str:
    sound = SOUND_REGEX.match(file)

    if sound is not None:
        return sound.group(1)

    return file


class AnkiDeck(object):
    def __init__(self, path: str) -> None:
        self.path: str = path
        self.zip = zipfile.ZipFile(path)

        dbfile, dbfilename = tempfile.mkstemp()
        os.close(dbfile)

        self.db_path = dbfilename

        self.save_db(dbfilename)

        self.db = sqlite3.connect(dbfilename)

        # Mapping from filename -> index
        self.media: Dict[str, str] = {}

        if self.exists("media"):
            with self.zip.open("media") as f:
                mapping = json.loads(f.read())
                self.media = {v: k for k, v in mapping.items()}

    def exists(self, path: str) -> bool:
        try:
            self.zip.open(path)
            return True
        except KeyError:
            return False

    def save_db(self, path: str) -> None:
        with self.zip.open("collection.anki2") as zipped:
            with open(path, "wb") as unzipped:
                unzipped.write(zipped.read())

    def find_note(self, mid: int, sort_field: str) -> Optional[NoteResult]:
        results = self.db.execute(
            """
            SELECT * from notes WHERE mid = ? AND sfld = ?
            """,
            (mid, sort_field),
        )

        row = results.fetchone()
        if row is None:
            return None

        return (row[1], split_fields(row[6]))

    def get_media(self, file: str) -> Optional[bytes]:
        normalized = normalize_media(file)

        if not normalized in self.media:
            return None

        real_file = self.media[normalized]

        if not self.exists(real_file):
            return None

        return self.zip.open(real_file).read()

    def get_models(self) -> Dict[str, Any]:
        (models_json_str,) = self.db.execute("SELECT models from col").fetchone()
        return json.loads(models_json_str)

    def get_decks(self) -> Dict[str, Any]:
        (decks_json_str,) = self.db.execute("SELECT decks from col").fetchone()
        return json.loads(decks_json_str)

    def __del__(self) -> None:
        try:
            os.unlink(self.db_path)
        except:
            pass


def lookup_field(anki: AnkiDeck, mid: int, field: int, sort_field: str) -> FieldResult:
    """
    Grab an existing field from an Anki deck.
    """
    row = anki.find_note(mid, sort_field)

    if row is None:
        return None

    _, fields = row

    if field >= len(fields):
        return None

    value = fields[field]

    if not SOUND_REGEX.match(value):
        return value

    normalized = normalize_media(value)

    # This is a media file
    data = anki.get_media(normalized)

    if data is None:
        return None

    return {
        "filename": normalized,
        "field": value,
        "data": data,
    }


def use_cached_field(anki: AnkiDeck, mid: int, field: int) -> FieldFunction[str]:
    """
    Transformer that can grab arbitary fields from an existing Anki deck.
    """
    return lambda sort_field: lookup_field(anki, mid, field, sort_field)


def lookup_guid(anki: AnkiDeck, mid: int, sort_field: str) -> Optional[str]:
    result = anki.find_note(mid, sort_field)

    if result is None:
        return None

    guid, _ = result
    return guid


def use_cached_guid(anki: AnkiDeck, mid: int) -> Callable[[str], Optional[str]]:
    return lambda a: lookup_guid(anki, mid, a)
