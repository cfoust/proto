from typing import Tuple, List

import proto

from proto.building import PathHelper, get_file_lines, sqlite
from proto.transforms import Forvo

from decks.ja.jmdict import JMDictGetter, JMReadingGetter

# Headword, POS
WordData = Tuple[str, str]


def generate_main(forvo: Forvo) -> None:
    """
    Generate the primary Japanese deck.
    """
    ph = PathHelper("ja")

    WordCard = proto.Model[WordData](
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

    deck = proto.Deck[WordData](
        "Japanese",
        [
            proto.Deck[WordData]("Adjectives", WordCard, adjectives),
            proto.Deck[WordData]("Nouns", WordCard, nouns),
            proto.Deck[WordData]("Verbs", WordCard, verbs),
        ],
    )

    if ph.target("ja.apkg"):
        deck.build("ja.apkg")
    if ph.target("ja-nomedia.apkg"):
        deck.build("ja-nomedia.apkg", media=False)


KanaData = str


def generate_alphabets(forvo: Forvo) -> None:
    ph = PathHelper("ja")

    CharacterCard = proto.Model[KanaData](
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

    deck = proto.Deck[KanaData](
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
