from typing import Tuple, List

import proto

from proto.building import PathHelper, get_file_lines
from proto.transforms import wrap_class, Forvo, pipe, CachedTransformer, priority
from proto.model import use_first_guid, default_guid
from proto.anki import AnkiDeck, use_cached_guid, use_cached_field
import json

# Headword, POS
WordData = Tuple[str, str]

def get_word_data(filename):
    lines = get_file_lines(filename)
    return list(map(lambda a: a.split("\t"), lines))

def get_headword(data: WordData) -> str:
    return data[0]

CODE = "zh"
FORVO = wrap_class(
    Forvo(
        CODE,
        limit_countries=["China", "Taiwan", "United States"]
    )
)

identity = lambda a: a

WORD_MID = 1556075006702

def generate_main() -> None:
    ph = PathHelper("zh")

    forvo = wrap_class(CachedTransformer[str](ph.db, "forvo", FORVO, identity))

    anki = AnkiDeck(ph.input("original.apkg", ignore=True))

    WordCard = proto.Model[WordData](
        WORD_MID,
        "zh-word",
        guid=pipe(
            (
                get_headword,
                priority([use_cached_guid(anki, WORD_MID), default_guid], ""),
            )
        ),
        fields=[
            proto.Field("Headword", get_headword),
            proto.Field(
                "Data",
                lambda data: json.dumps(data),
            ),
            proto.Field(
                "Sound",
                priority(
                    [
                        pipe((get_headword, use_cached_field(anki, WORD_MID, 2))),
                        pipe((get_headword, forvo)),
                    ],
                    None,
                ),
            ),
            proto.Field("POS", lambda data: data[-1],),
        ],
        templates=[
            {"name": "Card 1", "front": "{{Headword}}", "back": "{{Definition}}",}
        ],
    )

    verbs = get_word_data(ph.input("verbs"))
    nouns = get_word_data(ph.input("nouns"))
    adjectives = get_word_data(ph.input("adjectives"))

    deck = proto.Deck[WordData](
        1555986714664,
        "Mandarin",
        subdecks=[
            proto.Deck[WordData](1555986714733, "Adjectives", WordCard, adjectives),
            proto.Deck[WordData](1555986714665, "Nouns", WordCard, nouns),
            proto.Deck[WordData](1555986714710, "Verbs", WordCard, verbs),
        ],
    )

    if ph.target("zh.apkg"):
        deck.build("zh.apkg")

    if ph.target("zh-nomedia.apkg"):
        deck.build("zh-nomedia.apkg", include_media=False)


if __name__ == "__main__":
    generate_main()
