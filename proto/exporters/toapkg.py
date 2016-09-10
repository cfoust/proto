try:
    import anki
except:
    raise Exception('anki package not installed.')

from anki.storage import Collection
from anki.importing import TextImporter
from anki.exporting import AnkiPackageExporter
from tocsv import CSVExporter
import shutil, os, string

################################################
# Taken from http://stackoverflow.com/questions/1868714/how-do-i-copy-an-entire-directory-of-files-into-an-existing-directory-using-pyth
# Might as well be honest
################################################
def copytree(src, dst, symlinks=False, ignore=None):
    for item in os.listdir(src):
        s = os.path.join(src, item)
        d = os.path.join(dst, item)
        if os.path.isdir(s):
            shutil.copytree(s, d, symlinks, ignore)
        else:
            shutil.copy2(s, d)
################################################

class APKGExporter:
    @staticmethod
    def export(deck,filename,tmpPath = '',mediaPath = '',ignoreMedia = False):
        wdir = os.getcwd()

        def cleanFolder():
            os.chdir(wdir)
            # Cleans out the old tmp collection
            if os.path.exists(tmpPath + 'tmp.media'):
                shutil.rmtree(tmpPath + 'tmp.media')

            for f in ['tmp.media.db2','tmp.anki2','tmp.anki2-journal']:
                if os.path.exists(tmpPath + f):
                    try:
                        os.remove(tmpPath + f)
                    except:
                        continue

        cleanFolder()

        # Makes a new one
        tcol = Collection(tmpPath + 'tmp.anki2')

        os.chdir(wdir)

        # Copies media over

        if not ignoreMedia:
            copytree(mediaPath,tmpPath + 'tmp.media')

        os.chdir(wdir)

        # Sets up the decks and pulls them in

        def makeDeck(parent,prefix,deck):
            name = deck.csvname
            csvfile = "%s%s%s.csv" % (tmpPath,prefix,name)
            if not os.path.exists(csvfile) and deck.cardType != None:
                raise Exception('No csv file "' + csvfile + '" found.')

            did = tcol.decks.id(parent + deck.name)
            d = tcol.decks.get(did)
            tcol.decks.select(did)

            confId = tcol.decks.confId(parent + deck.name, cloneFrom=deck.conf)

            if not deck.cardType:
                conf = tcol.decks.getConf(confId)
                conf['new']['perDay'] = 999
                tcol.decks.updateConf(conf)
            elif deck.perDay:
                conf = tcol.decks.getConf(confId)
                conf['new']['perDay'] = deck.perDay
                tcol.decks.updateConf(conf)

            tcol.decks.setConf(d,confId)

            if deck.cardType:
                ct = deck.cardType

                if not tcol.models.byName(ct.name):
                    m = tcol.models.new(ct.name)
                    m['req'] = [[0, 'all', [0]]]
                    m['css'] = ct.css()
                    m['tmpls'] = [
                        {
                            'name': 'Card 1',
                            'qfmt': ct.front(),
                            'afmt': ct.back(),
                            'bfont': 'Lucida Sans Unicode',
                            'bamft': '',
                            'bqmft': '',
                            'ord': 0,
                            'did': None,
                            'bsize': 12
                        }
                    ]
                    tcol.models.add(m)

                    for i,field in enumerate(ct.fields):
                        f = tcol.models.newField(field.anki_name)
                        f['ord'] = i
                        tcol.models.addField(m,f)
                else:
                    m = tcol.models.byName(ct.name)

                # So that we can reuse already-present models
                # todo: this doesn't actually work but would be a big part of
                # updating
                # if m['id'] != ct.mid:
                # 	m = tcol.models.get(m['id'])
                # 	m['id'] = ct.mid
                # 	m.save(m)

                tcol.save()

                m['did'] = did
                tcol.decks.select(did)
                ti = TextImporter(tcol,csvfile)
                ti.model = m
                ti.allowHTML = True
                ti.initMapping()
                ti.delimiter = "\t"
                ti.updateDelimiter()

                ti.run()
                tcol.save()

            for sd in deck.subdecks:
                makeDeck(parent + deck.name + '::',prefix + name + '-', sd)

        makeDeck('','',deck)

        os.chdir(wdir)
        apkge = AnkiPackageExporter(tcol)
        apkge.includeSched = True
        apkge.exportInto(filename)

        cleanFolder()