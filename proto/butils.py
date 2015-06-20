"""Utilities used to make deck generation a lot easier and more streamlined."""
import os
from proto.exporters import APKGExporter
from progressbar import Bar, ProgressBar, Percentage, ETA


def Progress(data):
    """Iterates over a dataset normally, but prints a progress bar to the command line with an ETA."""

    pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=len(data)).start()

    for i, datum in enumerate(data):
        yield datum
        pbar.update(i + 1)

    pbar.finish()


class PathHelper:
    """Decides on a directory structure and database location for you automatically. Convenience class that handles
    pathing for you and lets you build .apkg files from a Deck.

    Stores proto's SQLite database in 'proto.db'.
    Stores media in 'media/[languagecode]/'.
    Stores output files (like decks and csvs) in 'output/[languagecode]/'

    Takes input files in at 'input/[languagecode]'.
    """

    db = 'proto.db'

    def __init__(self, code):
        """Takes in a ISO-639-1 language code and creates the directory structure."""

        self.output = 'output/%s/' % code
        os.makedirs(self.output)

        self.input = 'input/%s/' % code
        os.makedirs(self.input)

        self.media = 'media/%s/' % code
        os.makedirs(self.input)

        self.code = code

    def ifile(self, fileName):
        """Returns the relative path of the requested input file. For example, if you pass in 'asd.txt' and your
        language code is 'de', you would get back 'input/de/asd.txt' as long as the file exists."""

        p = self.input + fileName

        if os.path.exists(p):
            return p
        else:
            raise Exception('File %s not found in input directory.' % fileName)

    def ofile(self, fn):
        """Returns the relative path of the requested output file. See ifile(fileName) for details."""
        return self.output + fn

    def mfile(self, fn):
        """Returns the relative path of the requested media file. See ifile(fileName) for details."""
        # The path of the file
        p = self.media + fn

        if os.path.exists(p):
            return p
        else:
            raise Exception('File %s not found in media directory.' % fn)

    def apkgExport(self, deck, ignoreMedia=False):
        """The bread and butter of the PathHandler class. Exports a given deck into an .apkg file that
        can be directly imported into Anki and includes all media files. You must have generated all of
        the needed files before calling this. See method neededFiles(deck)."""
        deckPath = self.output + self.code + '.apkg'

        APKGExporter.export(deck, deckPath, self.output, self.media, ignoreMedia=ignoreMedia)

    def neededFiles(self, deck):
        """Returns a list of files that still need to be present before we can generate a deck. Recursively works
        through all the decks and subdecks."""
        def _neededFiles(pname, deck):
            needed = []
            if deck.cardType != None:
                csvfile = "%s-%s.csv" % (pname, deck.csvname)

                if not os.path.exists(self.ofile(csvfile)):
                    needed.append(csvfile)

            for subdeck in deck.subdecks:
                needed += _neededFiles(deck.csvname, subdeck)

            return needed

        return _neededFiles('', deck)


def fileLines(fn):
    """Gets the lines of a file with the given filename as a list of strings."""
    if os.path.isfile(fn):
        op = open(fn, 'r')
        lines = op.readlines()
        op.close()
        return [x.rstrip() for x in lines]
    else:
        return []


def loadTemplate(tname):
    """Loads a template from the templates directory and returns its contents."""
    p = 'templates/%s' % tname

    if os.path.exists(p):
        return open(p, 'r').read()
    else:
        raise Exception('Template %s not found in template directory.' % tname)


def applyDefaultTemplate(deck, recursive=True):
    """Applies proto's default CSS, JS, and HTML template to a deck with optional recursion."""

    if deck.cardType != None:
        deck.cardType._css = loadTemplate('proto.css')
        deck.cardType._js = loadTemplate('proto.js')
        deck.cardType._bheader = loadTemplate('proto.header.html')
        deck.cardType._bfooter = loadTemplate('proto.footer.html')

    if not recursive:
        return

    for sd in deck.subdecks:
        applyDefaultTemplate(sd)
