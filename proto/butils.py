"""Utilities used to make deck generation a lot easier and more streamlined."""
import os
from progressbar import Bar, ProgressBar, Percentage, ETA


def Progress(data):
    """Iterates over a dataset normally, but prints a progress bar to the 
        command line with an ETA."""

    pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=len(data)).start()

    for i, datum in enumerate(data):
        yield datum
        pbar.update(i + 1)

    pbar.finish()


class PathHelper:
    """Decides on a directory structure and database location for you 
        automatically. Convenience class that handles pathing for you and lets 
        you build .apkg files from a Deck.

        Stores proto's SQLite database in 'input/[languagecode]/[languagecode].db'.
        Stores media in 'media/[languagecode]/'.
        Stores output files (like decks and csvs) in 'output/[languagecode]/'

        Takes input files in at 'input/[languagecode]'.
    """

    def __init__(self, code):
        """Takes in a ISO-639-1 language code and creates 
           the directory structure."""
        
        self.code = code

        self._output = 'output/%s/' % code

        self._input = 'input/%s/' % code

        self._media = 'media/%s/' % code

        self._db = self._input + self.code + '.db'

        for folder in [self._media, self._input, self._output]:
            if not os.path.exists(folder):
                os.makedirs(folder)


    def db(self):
        return self._db

    def input(self, fileName):
        """Returns the relative path of the requested input file. For example, 
        if you pass in 'asd.txt' and your language code is 'de', you would get 
        back 'input/de/asd.txt' as long as the file exists."""

        # Return the folder path if there's no filename on the call
        if not fileName:
            return self._input

        p = self._input + fileName

        if os.path.exists(p):
            return p
        else:
            raise Exception('File %s not found in input directory.' % fileName)

    def output(self, fileName):
        """Returns the relative path of the requested output file. 
           See ifile(fileName) for details."""
        
        if not fileName:
            return self._output

        return self._output + fileName

    def media(self, fileName):
        """Returns the relative path of the requested media file. 
           See ifile(fileName) for details."""

        if not fileName:
            return self._media

        return self._media + fileName

    def apkgExport(self, deck, ignoreMedia=False):
        """The bread and butter of the PathHandler class. Exports a given deck 
        into an .apkg file that can be directly imported into Anki and includes 
        all media files. You must have generated all of the needed files before 
        calling this. See method neededFiles(deck)."""
        deckPath = self._output + self.code + '.apkg'

        #APKGExporter.export(deck, deckPath, self._output, self._media, ignoreMedia=ignoreMedia)

    def neededFiles(self, deck):
        """Returns a list of files that still need to be present before we can 
        generate a deck. Recursively works through all the decks and subdecks."""
        def _neededFiles(pname, deck):
            needed = []
            if deck.cardType:
                csvfile = "%s-%s.csv" % (pname, deck.csvname)

                if not os.path.exists(self.output(csvfile)):
                    needed.append(csvfile)

                # todo: check if the csv file has the right number of fields

            for subdeck in deck.subdecks:
                needed += _neededFiles(pname + '-' + deck.csvname if pname != '' else deck.csvname, subdeck)

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


def applyDefaultTemplate(deck, recursive=True, css='proto.css', js='proto.js', header='proto.header.html', footer='proto.footer.html'):
    """Applies proto's default CSS, JS, and HTML template to a deck with 
       optional recursion."""

    if deck.cardType != None:
        if css:
            deck.cardType._css = loadTemplate(css)
        if js:
            deck.cardType._js = loadTemplate(js)
        if header:
            deck.cardType._bheader = loadTemplate(header)
        if footer:
            deck.cardType._bfooter = loadTemplate(footer)

    if not recursive:
        return

    for sd in deck.subdecks:
        applyDefaultTemplate(sd)
