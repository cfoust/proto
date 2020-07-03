import proto

from proto.building import PathHelper, get_file_lines, sqlite
from proto.fields import Forvo

from decks.ja.jmdict import JMDictGetter, JMReadingGetter

def generate_main(forvo):
    """
    Generate the primary Japanese deck.
    """
    ph = PathHelper("ja")

    WordCard = proto.Model(
        1527532200,
        "ja-word",
        guid=lambda data: data[0],
        fields=[
            proto.Field("Headword", lambda data: data[0]),
            proto.Field("Reading", JMReadingGetter(ph.input("JmdictFurigana.txt"))),
            proto.Field("Definition", JMDictGetter(ph.input("JMdict_e"))),
            proto.Field("Sound", forvo),
            # The part of speech
            proto.Field("POS", lambda data: data[-1],),
        ],
        templates=[{"name": "Card 1", "front": "", "back": "",}],
    )

    verbs = get_file_lines(ph.input("verb-base.csv"))
    nouns = get_file_lines(ph.input("noun-base.csv"))
    adjectives = get_file_lines(ph.input("adj-base.csv"))

    deck = proto.Deck(
        "Japanese",
        [
            proto.Deck("Adjectives", WordCard, adjectives),
            proto.Deck("Nouns", WordCard, nouns),
            proto.Deck("Verbs", WordCard, verbs),
        ],
    )

    if ph.target("ja.apkg"):
        deck.build("ja.apkg")
    if ph.target("ja-nomedia.apkg"):
        deck.build("ja-nomedia.apkg", media=False)


def generate_alphabets(forvo):
    ph = PathHelper("ja")

    CharacterCard = proto.Model(
        1116319754,
        "ja-character",
        guid=lambda data: data[0],
        fields=[
            proto.Field("Character", lambda data: data[0]),
            proto.Field("Sound", forvo),
        ],
        templates=[{"name": "Card 1", "front": "", "back": "",}],
    )

    katakana = get_file_lines(ph.input("katakana.txt"))
    hiragana = get_file_lines(ph.input("hiragana.txt"))

    deck = proto.Deck(
        "Japanese-Kana",
        [
            proto.Deck("Katakana", CharacterCard, katakana),
            proto.Deck("Hiragana", CharacterCard, hiragana),
        ],
    )

    if ph.target("ja-kana.apkg"):
        deck.build("ja-kana.apkg")
    if ph.target("ja-kana-nomedia.apkg"):
        deck.build("ja-kana-nomedia.apkg", media=False)


if __name__ == "__main__":
    ph = PathHelper("ja")

    db = sqlite(ph.db)

    forvo = Forvo(
        db,
        "ja",
        limit_users=[
            "strawberrybrown",
            "skent",
            "akiko",
            "Emmacaron",
            "yasuo",
            "kaoring",
            "akitomo",
        ],
    )

    generate_main(forvo)
    generate_alphabets(forvo)
