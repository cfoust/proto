"""
Dump the decks and model JSON to stdout.
"""
import sys

from proto.anki import AnkiDeck

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2:
        print("wat are you doing")

    file = args[1]
    deck = AnkiDeck(file)

    models = deck.get_models()
    printed_models = {v["name"]: int(k) for k, v in models.items()}
    print(printed_models)

    decks = deck.get_decks()
    printed_decks = {v["name"]: int(k) for k, v in decks.items()}
    print(printed_decks)
