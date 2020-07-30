from typing import Tuple, List

import proto

from proto.building import PathHelper, get_file_lines
from proto.transforms import wrap_class, Forvo, pipe, CachedTransformer, priority
from proto.model import use_first_guid, default_guid
from proto.anki import AnkiDeck, use_cached_guid, use_cached_field

from decks.ja.jmdict import JMDictGetter, JMReadingGetter

# Headword, POS
WordData = Tuple[str, str]


def get_headword(data: WordData) -> str:
    return data[0]


def append_str(data: List[str], col: str) -> List[Tuple[str, str]]:
    return list(map(lambda v: (v, col), data))


FORVO = wrap_class(
    Forvo(
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
)

identity = lambda a: a


def generate_main() -> None:
    """
    Generate the primary Japanese deck.
    """
    ph = PathHelper("ja")

    forvo = wrap_class(CachedTransformer[str](ph.db, "forvo", FORVO, identity))

    anki = AnkiDeck(ph.input("ja-original.apkg", ignore=True))

    WordCard = proto.Model[WordData](
        1527532200,
        "ja-word",
        guid=pipe(
            (
                get_headword,
                priority([use_cached_guid(anki, 1527532200), default_guid], ""),
            )
        ),
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
                pipe(
                    (get_headword, wrap_class(JMDictGetter(ph.input("JMdict_e.xml"))))
                ),
            ),
            proto.Field(
                "Sound",
                priority(
                    [
                        pipe((get_headword, use_cached_field(anki, 1527532200, 2))),
                        pipe((get_headword, forvo)),
                    ],
                    None,
                ),
            ),
            # The part of speech
            proto.Field("POS", lambda data: data[-1],),
        ],
        templates=[{"name": "Card 1", "front": "", "back": "",}],
    )

    verbs = append_str(get_file_lines(ph.input("verb-base.csv")), "verb")
    nouns = append_str(get_file_lines(ph.input("noun-base.csv")), "noun")
    adjectives = append_str(get_file_lines(ph.input("adj-base.csv")), "adj")

    verbs = verbs[:10]
    nouns = []
    adjectives = []

    deck = proto.Deck[WordData](
        1475079952775,
        "Japanese",
        subdecks=[
            proto.Deck[WordData](1475079978856, "Adjectives", WordCard, adjectives),
            proto.Deck[WordData](1473292781966, "Nouns", WordCard, nouns),
            proto.Deck[WordData](1475079952775, "Verbs", WordCard, verbs),
        ],
    )

    if ph.target("ja.apkg"):
        deck.build("ja.apkg")

    if ph.target("ja-nomedia.apkg"):
        deck.build("ja-nomedia.apkg", include_media=False)


KanaData = str


def generate_alphabets() -> None:
    ph = PathHelper("ja")

    forvo = wrap_class(CachedTransformer[str](ph.db, "forvo-kana", FORVO, identity))

    CharacterCard = proto.Model[KanaData](
        1116319754,
        "ja-kana-character",
        guid=lambda data: data,
        fields=[
            proto.Field("Character", lambda data: data),
            proto.Field("Sound", forvo),
        ],
        templates=[{"name": "Card 1", "front": "", "back": "",}],
    )

    katakana = get_file_lines(ph.input("katakana.txt"))
    hiragana = get_file_lines(ph.input("hiragana.txt"))

    deck = proto.Deck[KanaData](
        1312855852,
        "Japanese-Kana",
        subdecks=[
            proto.Deck(1592761634, "Katakana", CharacterCard, katakana),
            proto.Deck(1403083956, "Hiragana", CharacterCard, hiragana),
        ],
    )

    if ph.target("ja-kana.apkg"):
        deck.build("ja-kana.apkg")
    if ph.target("ja-kana-nomedia.apkg"):
        deck.build("ja-kana-nomedia.apkg", include_media=False)


if __name__ == "__main__":
    ph = PathHelper("ja")

    generate_main()
    # generate_alphabets()
