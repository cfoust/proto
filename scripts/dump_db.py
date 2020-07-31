"""
Dump the database of an .apkg file somewhere.
"""
import sys

from proto.anki import AnkiDeck

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 3:
        print('wat are you doing')

    file = args[1]
    ofile = args[2]

    deck = AnkiDeck(file)
    deck.save_db(ofile)
