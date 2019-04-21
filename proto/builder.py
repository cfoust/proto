"""
Declares a Builder class that makes the process of generating decks a lot easier.
It associates data (headwords) with a deck so that all the user has to do
is provide those instead of handle all the nasty pathing code.
"""

from butils import PathHelper
from proto.exporters import CSVExporter

class Builder:
    """
    Convenience class for easy generation of decks. Removes the need to worry 
    about csv files being properly named and handles all the pathing 
    automatically, so that all the user has to do is provide a valid Anki deck 
    and language code. The rest is all handled.
    """

    headDeck = None
    languageCode = None
    deckTree = {}


    def __init__(self,languageCode,deck):
        """
        languageCode is the ISO-639-1 language code for the target language. 
        This can actually be any arbitrary string that is filesystem compliant, 
        as it is only passed to a path handler. deck is a proto.deck.Deck 
        instance.
        """
        self.languageCode = languageCode
        self.ph = PathHelper(languageCode)
        self.headDeck = deck
        self._makeTree()


    def _makeTree(self):
        """
        Internal function that sets up the tree of decks. This lets us store 
        the deck and its bound data all in one place and more easily check 
        whether we have everything ready. It isn't actually a tree, just a 
        dictionary, but it works similarly.
        """
        neededFiles = self.ph.neededFiles(self.headDeck)
        def appendDeck(parentName, parentCsvName, deck):
            # The Anki-style full name of the deck
            name = parentName + '::' + deck.name if parentName != '' else deck.name

            # The name of the corresponding csv file
            csvname = parentCsvName + '-' + deck.csvname if parentCsvName != '' else deck.csvname

            # Whether or not we need data for this (checked only once at builder initialization)
            needData = csvname + '.csv' in neededFiles

            self.deckTree[name] = {
                'csvname': csvname,
                'needData': needData,
                'deck': deck,
                'data': []
            }

            # Recursion
            for subdeck in deck.subdecks:
                appendDeck(name,csvname,subdeck)

        # Calls appendDeck for the main deck
        appendDeck('', '', self.headDeck)


    def deckNeedsData(self, deckName):
        """
        Returns true if a deck needs data. 'Data' here really means 
        headwords (lemmas). deckName is the Anki-style deck name, so something 
        like "German::Nouns" would work. In this case, 'German' is the parent
        deck and Nouns is the child deck that actually has generated cards.
        """

        if not deckName in self.deckTree:
            raise Exception('No such deck: %s' % deckName)

        deckObject = self.deckTree[deckName]['needData']
        return deckObject['needData'] and len(deckObject['data']) == 0


    def needAnyData(self):
        """
        Returns true if any deck needs data.
        """
        for deck in self.deckTree:
            if self.deckTree[deck]['needData']:
                return True
        return False


    def bindDeckData(self, deckName, data):
        """
        Binds an array of data to the deck with the corresponding Anki name.

        For example:
        builder.bindDeckData("Russian::Nouns", wordList)
        """

        if not deckName in self.deckTree:
            raise Exception('No such deck: %s' % deckName)

        self.deckTree[deckName]['data'] = data


    def build(self, ignoreMedia = False):
        """
        Generates all the necessary cards and builds the Anki .apkg file.
        """

        for deckName in self.deckTree:
            # Get the deck object.
            deckObject = self.deckTree[deckName]

            # Make variables for its properties.
            name = deckName
            deck = deckObject['deck']
            data = deckObject['data']

            # Skip this deck if we don't need to generate anything.
            if not deckObject['needData']:
                continue

            if len(data) == 0:
                print 'Deck %s needs data and has none. Skipping.' % name
                continue

            print 'Building cards for deck %s.' % name

            for word in Progress(data):
                result = deck.makeCard(word)

            print 'Generated %d/%d cards.' % (len(deck.cardType.cards), len(data))

            """We output to a .csv because this is what Anki (or in this case,
                the Anki library) imports into the collection."""
            CSVExporter.export(deck,self.ph.output(deckObject['csvname'] + '.csv'))

        self.ph.apkgExport(self.headDeck, ignoreMedia=ignoreMedia)
        print 'Build of %s successful.' % self.headDeck.name
