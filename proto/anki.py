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

from typing import List, Dict, Optional, Generic, TypeVar, Tuple

# guid, fields
NoteResult = Tuple[str, List[str]]

SOUND_REGEX = re.compile("\[sound:(.+)\]")


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

        with self.zip.open("collection.anki2") as zipped:
            with open(dbfilename, "wb") as unzipped:
                unzipped.write(zipped.read())

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

        return (row[1], row[6].split("\x1f"))

    def get_media(self, file: str) -> Optional[bytes]:
        normalized = normalize_media(file)

        if not normalized in self.media:
            return None

        real_file = self.media[normalized]

        if not self.exists(real_file):
            return None

        return self.zip.open(real_file).read()

    def __del__(self) -> None:
        try:
            os.unlink(self.db_path)
        except:
            pass
