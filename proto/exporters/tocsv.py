import csv

class CSVExporter:
    @staticmethod
    def export(deck,filename,delimiter = '\t'):
        if not deck.cardType:
            raise Exception('Deck has no card type.')

        with open(filename, 'w') as f:
            writer = csv.writer(f, dialect='excel-tab')

            for card in deck.cardType.cards:
                fixed = []
                for field in card:
                    if field is None:
                        field = ""

                    fixed.append(field)

                writer.writerow(fixed)
