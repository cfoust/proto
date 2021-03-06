import peewee, datetime, zlib, base64


class FieldType:
    """ Name as it will show up in Anki for this field. 
        Does not need to be unique."""
    anki_name = "Basic Field"

    """ Encapsulates the text that is generated by this class. 
        Mostly for convenience."""
    html = """<div class="content center">%s</div>"""

    # Text to be appended to the card CSS for this field.
    css = ""

    # Text to be appended to the card JS for this field.
    js = ""

    order = -1

    # Whether or not this field shows up on the front of the card.
    front = False

    def __init__(self,front = False):
        self.front = front

    """Always generated for the basic class, no caching. The pull method just 
       takes the word input and returns the formatted output for the desired 
       field."""
    def pull(self,word):
        return word

"""This makes it so you can use multiple field generators for a given field.
   The fields are iterated over in the order added. If a field returns a
   value, the PriorityFieldType returns that value and stops iteration."""
class PriorityFieldType(FieldType):

    def __init__(self,fields):
        assert len(fields) > 0
        self.fields = fields

    def pull(self,word):
        for subfield in self.fields:
            result = subfield.pull(word)
            if result != None:
                return result
        return None

# Standin proxy for a potential peewee database
dbproxy = peewee.Proxy()

class CachedInfo(peewee.Model):
    """This is the model that we use so peewee can store cached information
       in the database. We automatically compress when above a certain size
       threshold."""

    db_name = peewee.CharField()
    timestamp = peewee.DateTimeField()
    lemma = peewee.CharField()
    data = peewee.TextField()
    compressed = peewee.BooleanField()
    class Meta:
        database = dbproxy

""" Number of characters after which we compress. """
COMPRESSION_CUTOFF = 1024
class Cacher:
    def __init__(self, db, identifier):
        """Makes a connection to the provided peewee db."""
        db.connect()
        dbproxy.initialize(db)

        self.db = db

        # Create the tables if they don't exist
        self.db.create_tables([CachedInfo],safe=True)

        """The identifier is a unique string that all data cached by this
           instance uses to differentiate from other caches in the database."""
        self.identifier = identifier

    def _getRow(self,word):
        return CachedInfo.get(CachedInfo.db_name == self.identifier,
                              CachedInfo.lemma == word)

    """ Checks whether some data exists for a word. """
    def exists(self,word):
        try:
            info = self._getRow(word)
            return True
        except peewee.DoesNotExist:
            return False

    """ Pulls some cached info from the DB. """
    def retrieve(self,word):
        try:
            info = self._getRow(word)
            if info.compressed:
                return zlib.decompress(base64.b64decode(info.data))
            else:
                return info.data
        except peewee.DoesNotExist:
            return None

    """ This can create new entries or update old ones."""
    def store(self,word,data):

        compressed = len(data) > COMPRESSION_CUTOFF
        if compressed:
            data = base64.b64encode(zlib.compress(data))

        # If data for the word already exists in the database, update it
        if self.exists(word):
            info = self._getRow(word)
            info.compressed = compressed
            info.data = data
            info.timestamp = datetime.datetime.now()
            info.save()
        # Otherwise create a new entry
        else:
            info = CachedInfo.create(db_name = self.identifier,
                                     timestamp = datetime.datetime.now(),
                                     lemma = word,
                                     data = data,
                                     compressed = compressed)

    """Convenience method that imports data en masse. Each entry in the 'data'
       parameter is a tuple such that (input,output)."""
    def storeMany(self,data):
        transformed = []

        # We create a provincial array to add all our metadata
        # todo: is this actually being compressed? no
        for word,datum in data:
            compressed = len(datum) > COMPRESSION_CUTOFF
            transformed.append({
                'compressed': compressed,
                'data': datum,
                'timestamp': datetime.datetime.now(),
                'db_name': self.identifier,
                'lemma': word
            })

        # db.atomic is much faster for many writes
        with self.db.atomic():
            CachedInfo.insert_many(transformed).execute()


    """Deletes all data for a given word/lemma."""
    def delete(self,word):
        info = self._getRow(word)
        info.delete_instance()

    """Wipes all of the rows with this Cacher's identifier."""
    def clear(self):
        CachedInfo.delete().where(CachedInfo.db_name == self.identifier).execute()

    """Renames the identifier used by this Cacher. Does not check for conflicts
       on purpose, as we occasionally want to combine datasets."""
    def rename(self,newname):
        CachedInfo.update(db_name=newname).where(CachedInfo.db_name == self.identifier).execute()
        self.identifier = newname


"""This field type automatically caches the results of its 'generate' function.
   Very good for pulling data from websites or sources that require a lot of
   time for each word. Does not cache None results."""
class CacheableFieldType(FieldType):
    """ Just for cached fields, how the name will show up in the DB. 
        Needs to be unique or will conflict with other data."""
    db_name = "cacheable-default"

    def __init__(self,pathToDb):
        self.cacher = Cacher(pathToDb, self.db_name)

    def pull(self,word):
        if self.cacher.exists(word):
            result = self.cacher.retrieve(word)
            return result
        else:
            result = self.generate(word)

            if not result:
                return None

            self.cacher.store(word,result)
            return result

    """ Generates the resulting string given the input. 
        May be computationally expensive because this is cacheable."""
    def generate(self,word):
        return word

"""Field type that just returns the string provided to it on
initialization. Useful for generic card types that need some data
affixed to eery card."""
class StaticFieldType(FieldType):
    def __init__(self, staticString):
        self.staticString = staticString

    def pull(self,word):
        return self.staticString

switchHTML = """
<div id='left-mean-%s' style='display:none'>{{%s}}</div>
<div id='right-mean-%s' style='display:none'>{{%s}}</div>

<button id="left-button-%s" class="content-button left-button">%s</button>
<button id="right-button-%s"  class="content-button right-button">%s</button>
<div class="top-cut content" id='switch-content-%s'>none</div>
"""

switchJS = """
var left = document.getElementById('left-button-%s');

var selectLeft = function() {
    var text = document.getElementById('left-mean-%s').innerHTML;
    var leftClasses = "content-button left-button content-button-selected";
    var rightClasses = "content-button right-button";

    document.getElementById('switch-content-%s').innerHTML = text;
    document.getElementById('left-button-%s').className = leftClasses;
    document.getElementById('right-button-%s').className = rightClasses;
}

left.onclick = selectLeft;
left.touchstart = selectLeft;

var right = document.getElementById('right-button-%s');

var selectRight = function() {
    var text = document.getElementById('right-mean-%s').innerHTML;
    var rightClasses = "content-button right-button content-button-selected";
    var leftClasses = "content-button left-button";

    document.getElementById('switch-content-%s').innerHTML = text;
    document.getElementById('left-button-%s').className = leftClasses;
    document.getElementById('right-button-%s').className = rightClasses;
}

right.onclick = selectRight;
right.touchstart = selectRight;

selectLeft();
"""
import random
def Switchable(leftLabel, rightLabel, left, right):
    """Turns two fields that would normally display as separate boxes on the card
    into one content box. On top are buttons, labeled leftLabel and rightLabel,
    that the user can press to switch the content box's content.

    The left content is shown by default.

    You should add CSS styles for left-button, right-button, content-button,
    and content-button-selected."""

    # Used for making sure there's no collision between switchable frames
    # if there are multiple on one card
    suffix = str(random.randint(0,1000))

    # formats the html
    html = switchHTML % (suffix, 
                         left.anki_name, 
                         suffix, 
                         right.anki_name,
                         suffix,
                         leftLabel,
                         suffix,
                         rightLabel,
                         suffix)
    # formats the js
    js = switchJS.replace('%s',suffix)

    left.html = ""
    left.js = ""

    right.html = html
    right.js = js