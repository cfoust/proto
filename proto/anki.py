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

from typing import List, Optional, Generic, TypeVar, Tuple

# guid, fields
NoteResult = Tuple[str, List[str]]

class AnkiDeck(object):

    def __init__(self, path: str) -> None:
        self.path: str = path
        self.zip = zipfile.ZipFile(path)

        dbfile, dbfilename = tempfile.mkstemp()
        os.close(dbfile)

        self.db_path = dbfilename

        with self.zip.open('collection.anki2') as zipped:
            with open(dbfilename, 'wb') as unzipped:
                unzipped.write(zipped.read())

        self.db = sqlite3.connect(dbfilename)


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

        return (row[1], row[6].split('\x1f'))


    def __del__(self) -> None:
        try:
            os.unlink(self.db_path)
        except:
            pass
