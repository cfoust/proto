import csv, os


class CSVImporter:
    @staticmethod
    def importIntoDeck(deck,file,delimiter = '\t'):
        if not os.path.exists(file):
            raise Exception('Input csv %s does not exist' % file)

        csvfile = open(file,'rb')
        reader = csv.reader(csvfile,delimiter = delimiter, dialect='excel-tab')

        data = [line for line in reader]
        if len(data) == 0:
            raise Exception('CSV file %s had no data.' % file)
        if len(data[0]) != len(deck.cardType.fields):
            raise Exception('CSV file %s has invalid number of fields for deck.' % file)

        deck.cardType.cards += data
