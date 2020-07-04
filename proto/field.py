import peewee
import datetime
import zlib
import base64

from typing import (
    Callable,
    Dict,
    Generic,
    Iterable,
    List,
    Optional,
    TypeVar,
    Union,
    Tuple,
)

Data = TypeVar("Data")

# This is the type all fields must return.
FieldData = Union[str, bytes]
FieldResult = Optional[FieldData]
FieldFunction = Callable[[Data], FieldResult]


class Field(Generic[Data]):
    """
    Base class that manages transforming card data for a field.
    """

    def __init__(self, name: str, transform: Callable[[Data], FieldResult]) -> None:
        self.name = name
        self.transform = transform
        pass

    def run(self, data: Data) -> FieldResult:
        return self.transform(data)


# Standin proxy for a potential peewee database
dbproxy = peewee.Proxy()


class CachedInfo(peewee.Model):
    """This is the model that we use so peewee can store cached information
       in the database. We automatically compress when above a certain size
       threshold."""

    db_name = peewee.CharField()
    timestamp = peewee.DateTimeField()
    key = peewee.TextField()
    data = peewee.BlobField()
    is_string = peewee.BooleanField()

    class Meta:
        database = dbproxy


""" Number of characters after which we compress. """
COMPRESSION_CUTOFF = 1024


def pack_data(data: FieldData) -> bytes:
    if isinstance(data, str):
        data = data.encode("utf-8")

    return zlib.compress(data)


def unpack_data(data: bytes, is_string: bool) -> FieldData:
    blob = zlib.decompress(data)
    if not is_string:
        return blob
    return blob.decode("utf-8")


class Cacher:
    def __init__(self, db_path: str, identifier: str):
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
            CachedInfo.db_name == self.identifier, CachedInfo.lemma == key
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

    def retrieve(self, key: str) -> Optional[Tuple[datetime.datetime, FieldData]]:
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

    def store(self, key: str, data: FieldData) -> None:
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

    def store_many(self, data: List[Tuple[str, FieldResult]]) -> None:
        """
        Convenience method that imports data en masse. Each entry in the 'data'
        parameter is a tuple such that (input,output).
        """
        transformed = []

        # We create a temporary array to add all our metadata
        for key, datum in data:
            datum = "[nothing]" if datum is None else datum
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
        Wipes all of the rows with this Cacher's identifier.
        """
        CachedInfo.delete().where(CachedInfo.db_name == self.identifier).execute()

    def rename(self, new_name: str) -> None:
        """
        Renames the identifier used by this Cacher. Does not check for
        conflicts on purpose, as we occasionally want to combine datasets.
        """
        CachedInfo.update(db_name=new_name).where(
            CachedInfo.db_name == self.identifier
        ).execute()
        self.identifier = new_name


class CacheableField(Generic[Data]):
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
        # Takes Data and returns a string we can use as a unique key.
        # Often this is just the word itself.
        transformer: Callable[[Data], str],
        field: Field[Data],
        # The amount of time we should wait before trying to call
        # the field again after it returns None initially.
        retry: datetime.timedelta = datetime.timedelta(weeks=2),
    ):
        super().__init__()
        self.db_name: str = "cacheable-default"
        self.cacher: Cacher = Cacher(db_path, self.db_name)
        self.retry = retry
        self.transformer = transformer
        self.field = field

    def run(self, data: Data):
        key = self.transformer(data)

        if not self.cacher.exists(key):
            result = self.field.run(data)

            # Make a note if the generator returned None so we don't pull again
            # for awhile
            if not result:
                self.cacher.store(key, "[nothing]")
                return None

            self.cacher.store(key, result)
            return result

        row = self.cacher.retrieve(key)

        # Should never happen
        if not row:
            return None

        timestamp, result = row

        # If the call originally returned nothing
        # I recognize this is a terrible idea, but it's just not a big deal
        if result == "[nothing]":
            # If we've passed the cache date, we can try again
            if (timestamp + self.retry) < datetime.datetime.now():
                # Delete the cache
                self.cacher.delete(key)

                # We just pull again
                return self.run(data)

            # Otherwise return None
            return None

        return result
