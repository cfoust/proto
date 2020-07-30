"""
Contains generalized caching logic for all of proto's datatypes.
"""

import sqlite3
import datetime
import zlib
import json

from typing import Union, Optional, Tuple, List, Callable
from proto.field import FieldResult

RowType = Tuple[
    # type
    str,
    # timestamp
    datetime.datetime,
    # key
    str,
    # is_media
    bool,
    # media_json
    Optional[str],
    # data
    Optional[bytes],
]

PackType = Tuple[
    bool, Optional[str], Optional[bytes],
]


def pack_data(data: FieldResult) -> PackType:
    if data is None:
        return (False, None, None)

    if isinstance(data, str):
        return (False, None, data.encode("utf-8"))

    # Has to be media
    return (
        True,
        json.dumps({"filename": data["filename"], "field": data["field"],}),
        zlib.compress(data["data"]),
    )


def unpack_data(data: PackType) -> FieldResult:
    is_media, media_json, blob = data

    if is_media:
        # Something is off
        if media_json is None or blob is None:
            return None

        dejson = json.loads(media_json)
        return {
            "filename": dejson["filename"],
            "field": dejson["field"],
            "data": zlib.decompress(blob),
        }

    if blob is None:
        return None

    # Otherwise it's a string
    return blob.decode("utf-8")


class Cache:
    """
    Simple SQlite caching mechanism.
    """

    def __init__(
        self,
        # The path to the SQLite database.
        db_path: str,
        # The 'namespace' for all entries stored using this class instance.
        identifier: str,
    ):
        db = sqlite3.connect(db_path, detect_types=sqlite3.PARSE_DECLTYPES)

        db.execute(
            """
CREATE TABLE IF NOT EXISTS proto_cache (
    -- The "namespace" of the row
    type TEXT NOT NULL,
    -- When the row was last updated
    timestamp TIMESTAMP NOT NULL,
    -- The primary key of the individual row
    key TEXT NOT NULL,
    -- Whether the blob is a media blob
    is_media BOOLEAN NOT NULL,
    -- This contains the Media dict if is_media is True
    media_json TEXT,
    -- If is_media, contains the media file, otherwise this is the string.
    data BLOB
)
        """
        )
        db.commit()

        self.db = db

        """The identifier is a unique string that all data cached by this
           instance uses to differentiate from other caches in the database."""
        self.identifier = identifier

    def _get_row(self, key: str) -> Optional[RowType]:
        results = self.db.execute(
            """
SELECT * from proto_cache WHERE type = ? AND key = ?
""",
            (self.identifier, key),
        )

        return results.fetchone()

    def exists(self, key: str) -> bool:
        """
        Checks whether some data exists for a key.
        """
        return self._get_row(key) is not None

    def retrieve(self, key: str) -> Optional[Tuple[datetime.datetime, FieldResult]]:
        """
        Pulls some cached info from the DB.

        Returns a tuple of (timestamp, data) if the word exists and None if
        it does not.
        """
        # Grab the word from the database
        row = self._get_row(key)

        if not row:
            return None

        identifier, ts, key, is_media, media_json, data = row

        value = unpack_data((is_media, media_json, data))

        # Return the data and its timestamp.
        return (ts, value)

    def _upsert(self, values: List[RowType]):
        self.db.executemany(
            """
INSERT OR REPLACE INTO proto_cache (
    type,
    timestamp,
    key,
    is_media,
    media_json,
    data
) VALUES (?, ?, ?, ?, ?, ?)
        """,
            values,
        )
        self.db.commit()

    def store(self, key: str, data: FieldResult) -> None:
        """
        This can create new entries or update old ones.
        """

        is_media, media_json, blob = pack_data(data)

        self._upsert(
            [
                (
                    self.identifier,
                    datetime.datetime.now(),
                    key,
                    is_media,
                    media_json,
                    blob,
                )
            ]
        )

    def store_many(self, data: List[Tuple[str, FieldResult]]) -> None:
        """
        Convenience method that imports data en masse. Each entry in the 'data'
        parameter is a tuple such that (input,output).
        """
        transformed: List[RowType] = []

        # We create a temporary array to add all our metadata
        for key, datum in data:
            is_media, media_json, blob = pack_data(datum)
            transformed.append(
                (
                    self.identifier,
                    datetime.datetime.now(),
                    key,
                    is_media,
                    media_json,
                    blob,
                )
            )

        self._upsert(transformed)

    def delete(self, key: str) -> None:
        """
        Deletes all data for a given key.
        """
        self.db.execute(
            """
DELETE FROM proto_cache WHERE type = ? AND key = ?
        """,
            (self.identifier, key,),
        )
        self.db.commit()

    def clear(self) -> None:
        """
        Wipes all of the rows with this Cache's identifier.
        """
        self.db.execute(
            """
DELETE FROM proto_cache WHERE type = ?
        """,
            (self.identifier,),
        )
        self.db.commit()

    def rename(self, new_name: str) -> None:
        """
        Renames the identifier used by this Cache. Does not check for
        conflicts on purpose, as we occasionally want to combine datasets.
        """
        raise Exception("todo")
