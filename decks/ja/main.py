from typing import Tuple, List

import proto

from proto.building import PathHelper, get_file_lines, sqlite
from proto.transforms import wrap_class, Forvo, pipe

from decks.ja.jmdict import JMDictGetter, JMReadingGetter

# Headword, POS
WordData = Tuple[str, str]


def get_headword(data: WordData) -> str:
    return data[0]


def append_str(data: List[str], col: str) -> List[Tuple[str, str]]:
    return list(map(lambda v: (v, col), data))


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
            proto.Field("Headword", get_headword),
            proto.Field(
                "Reading",
                pipe(
                    (
                        get_headword,
                        wrap_class(JMReadingGetter(ph.input("JmdictFurigana.txt"))),
                    )
                ),
            ),
            proto.Field(
                "Definition",
                pipe((get_headword, wrap_class(JMDictGetter(ph.input("JMdict_e.xml"))))),
            ),
            proto.Field("Sound", pipe((get_headword, wrap_class(forvo)))),
            # The part of speech
            proto.Field("POS", lambda data: data[-1],),
        ],
        templates=[{"name": "Card 1", "front": "", "back": "",}],
    )

    verbs = append_str(get_file_lines(ph.input("verb-base.csv")), "verb")
    nouns = append_str(get_file_lines(ph.input("noun-base.csv")), "noun")
    adjectives = append_str(get_file_lines(ph.input("adj-base.csv")), "adj")

    deck = proto.Deck[WordData](
        "Japanese",
        subdecks=[
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
        "ja-kana-character",
        guid=lambda data: data,
        fields=[
            proto.Field("Character", lambda data: data),
            proto.Field("Sound", wrap_class(forvo)),
        ],
        templates=[{"name": "Card 1", "front": "", "back": "",}],
    )

    katakana = get_file_lines(ph.input("katakana.txt"))
    hiragana = get_file_lines(ph.input("hiragana.txt"))

    deck = proto.Deck[KanaData](
        "Japanese-Kana",
        subdecks=[
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
