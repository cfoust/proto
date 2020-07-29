import datetime
import zlib
import peewee

from typing import (
    Union, Optional, Tuple, List, Callable
)
from proto.field import FieldResult

# Standin proxy for a potential peewee database
dbproxy = peewee.Proxy()


class CachedInfo(peewee.Model):
    """This is the model that we use so peewee can store cached information
       in the database. We automatically compress when above a certain size
       threshold."""

    db_name = peewee.CharField()
    timestamp = peewee.DateTimeField()
    key = peewee.TextField()
    data = peewee.BlobField(null=True)
    is_string = peewee.BooleanField()

    class Meta:
        database = dbproxy


CacheData = Union[str, bytes, None]


def pack_data(data: CacheData) -> Optional[bytes]:
    if not data:
        return None

    if isinstance(data, str):
        data = data.encode("utf-8")

    return zlib.compress(data)


def unpack_data(data: Optional[bytes], is_string: bool) -> CacheData:
    if not data:
        return None

    blob = zlib.decompress(data)
    if not is_string:
        return blob

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
        """Makes a connection to the provided peewee db."""
        db = peewee.SqliteDatabase(db_path)
        db.connect(reuse_if_open=True)
        dbproxy.initialize(db)

        self.db = db

        # Create the tables if they don't exist
        self.db.create_tables([CachedInfo], safe=True)

        """The identifier is a unique string that all data cached by this
           instance uses to differentiate from other caches in the database."""
        self.identifier = identifier

    def _get_row(self, key: str):
        return CachedInfo.get(
            CachedInfo.db_name == self.identifier, CachedInfo.key == key
        )

    def exists(self, key: str) -> bool:
        """
        Checks whether some data exists for a key.
        """

        try:
            info = self._get_row(key)
            return True
        except peewee.DoesNotExist:
            return False

    def retrieve(self, key: str) -> Optional[Tuple[datetime.datetime, CacheData]]:
        """
        Pulls some cached info from the DB.

        Returns a tuple of (timestamp, data) if the word exists and None if
        it does not.
        """
        try:
            # Grab the word from the database
            info = self._get_row(key)
            value = unpack_data(info.data, info.is_string)

            # Return the data and its timestamp.
            return (info.timestamp, value)
        except peewee.DoesNotExist:
            return None

    def store(self, key: str, data: CacheData) -> None:
        """
        This can create new entries or update old ones.
        """
        is_string = type(data) is str
        value = pack_data(data)

        # If data for the key already exists in the database, update it
        if self.exists(key):
            info = self._get_row(key)
            info.is_string = is_string
            info.data = value
            info.timestamp = datetime.datetime.now()
            info.save()
        # Otherwise create a new entry
        else:
            info = CachedInfo.create(
                db_name=self.identifier,
                timestamp=datetime.datetime.now(),
                key=key,
                data=value,
                is_string=is_string,
            )

    def store_many(self, data: List[Tuple[str, CacheData]]) -> None:
        """
        Convenience method that imports data en masse. Each entry in the 'data'
        parameter is a tuple such that (input,output).
        """
        transformed = []

        # We create a temporary array to add all our metadata
        for key, datum in data:
            blob = pack_data(datum)
            is_string = type(datum) is str
            transformed.append(
                {
                    "is_string": is_string,
                    "data": blob,
                    "timestamp": datetime.datetime.now(),
                    "db_name": self.identifier,
                    "key": key,
                }
            )

        # db.atomic is much faster for many writes
        with self.db.atomic():
            CachedInfo.insert_many(transformed).execute()

    def delete(self, key: str) -> None:
        """
        Deletes all data for a given key.
        """
        info = self._get_row(key)
        info.delete_instance()

    def clear(self) -> None:
        """
        Wipes all of the rows with this Cache's identifier.
        """
        CachedInfo.delete().where(CachedInfo.db_name == self.identifier).execute()

    def rename(self, new_name: str) -> None:
        """
        Renames the identifier used by this Cache. Does not check for
        conflicts on purpose, as we occasionally want to combine datasets.
        """
        CachedInfo.update(db_name=new_name).where(
            CachedInfo.db_name == self.identifier
        ).execute()
        self.identifier = new_name


class TimeCache(object):
    """
    This field type automatically caches the results of its 'generate'
    function.  Very good for pulling data from websites or sources that require
    a lot of time for each word. Remembers the last time that the method
    returned None and does not call generate again until after a certain
    timedelta.
   """

    def __init__(
        self,
        db_path: str,
        identifier: str,
        generator: Callable[[str], CacheData],
        # The amount of time we should wait before trying to call
        # the field again after it returns None initially.
        retry: datetime.timedelta = datetime.timedelta(weeks=2),
    ):
        super().__init__()
        self.cacher: Cache = Cache(db_path, identifier)
        self.retry = retry
        self.generator = generator

    def call(self, data: str) -> FieldResult:
        if not self.cacher.exists(data):
            result = self.generator(data)
            self.cacher.store(data, result)
            return result

        row = self.cacher.retrieve(data)

        # Should never happen
        if not row:
            return None

        timestamp, result = row

        if result is None:
            # If we've passed the cache date, we can try again
            if (timestamp + self.retry) < datetime.datetime.now():
                # Delete the cache
                self.cacher.delete(data)

                # We just pull again
                return self.call(data)

            # Otherwise return None
            return None

        return result
