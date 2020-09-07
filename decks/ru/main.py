import proto

from proto.building import PathHelper, get_file_lines
from proto.transforms import wrap_class, Forvo, pipe, CachedTransformer, priority
from proto.model import use_first_guid, default_guid
from proto.anki import AnkiDeck, use_cached_guid, use_cached_field

import json, os

MODELS = {"WORD": 1468192145778, "VERB": 1468192152106}
DECKS = {
    "MAIN": 1593197985966,
    "NOUNS": 1593197985967,
    "ADJECTIVES": 1593197986151,
    "VERBS": 1593197986229,
}

WordData = str

ph = PathHelper("ru")


CODE = "ru"


def generate_main() -> None:
    ph = PathHelper(CODE)

    forvo = wrap_class(
        CachedTransformer[str](ph.db, "forvo", wrap_class(Forvo(CODE)), lambda a: a)
    )

    anki = AnkiDeck(ph.input("originals/%s.apkg" % (CODE), ignore=True))

    nouns = get_file_lines(ph.input("RussianNouns.csv"))
    adjectives = get_file_lines(ph.input("RussianAdjectives.csv"))
    verbs = get_file_lines(ph.input("RussianVerbs.csv"))

    WordCard = proto.Model[WordData](
        MODELS["WORD"],
        "ru-word",
        guid=priority([use_cached_guid(anki, MODELS["WORD"]), default_guid], ""),
        fields=[
            proto.Field("Headword", identity),
            proto.Field("En_Meaning", use_cached_field(anki, MODELS["WORD"], 2)),
            proto.Field("Ru_Meaning", use_cached_field(anki, MODELS["WORD"], 3)),
            proto.Field("Audio", use_cached_field(anki, MODELS["WORD"], 4)),
        ],
        templates=[
            {"name": "Card 1", "front": "{{Headword}}", "back": "{{Definition}}",}
        ],
    )

    VerbCard = proto.Model[WordData](
        MODELS["VERB"],
        "ru-verb",
        guid=priority([use_cached_guid(anki, MODELS["VERB"]), default_guid], ""),
        fields=[
            proto.Field("Imperfective", use_cached_field(anki, MODELS["VERB"], 0)),
            proto.Field("Perfective", use_cached_field(anki, MODELS["VERB"], 1)),
            proto.Field("En_Meaning", use_cached_field(anki, MODELS["VERB"], 2)),
            proto.Field("Ru_Meaning", use_cached_field(anki, MODELS["VERB"], 3)),
            proto.Field("Audio", use_cached_field(anki, MODELS["VERB"], 4)),
        ],
        templates=[
            {"name": "Card 1", "front": "{{Headword}}", "back": "{{Definition}}",}
        ],
    )

    deck = proto.Deck[WordData](
        DECKS["MAIN"],
        "Russian",
        subdecks=[
            proto.Deck[WordData](
                DECKS["ADJECTIVES"], "Adjectives", WordCard, adjectives
            ),
            proto.Deck[WordData](DECKS["NOUNS"], "Nouns", WordCard, nouns),
            proto.Deck[WordData](DECKS["VERBS"], "Verbs", WordCard, verbs),
        ],
    )

    if ph.target("%s.apkg" % CODE):
        deck.build("%s.apkg" % CODE)

    if ph.target("%s-nomedia.apkg" % CODE):
        deck.build("%s-nomedia.apkg" % CODE, include_media=False)


if __name__ == "__main__":
    generate_main()
