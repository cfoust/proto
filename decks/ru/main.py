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

def grab_column(pos: str, cols: List[List[str]]) -> List[str]:
    """
    Strip off a unique list from the list of words.
    """
    return list(set(list(map(lambda row: row[2], filter(lambda row: row[3] == pos, words)))))


def generate_main() -> None:
    ph = PathHelper("ja")

    forvo = wrap_class(
        CachedTransformer[str](ph.db, "forvo", wrap_class(Forvo("ru",)), lambda a: a)
    )

    anki = AnkiDeck(ph.input("originals/ru.apkg", ignore=True))

    words = get_file_lines(ph.input("lemma.num")).split(' ')

    nouns = grab_column('noun', words)
    verbs = grab_column('verb', words)
    adjectives = grab_column('adj', words)

    WordCard = proto.Model[WordData](
        MODELS["WORD"],
        "ru-word",
        guid=priority([use_cached_guid(anki, MODELS["WORD"]), default_guid], ""),
        fields=[],
        templates=[
            {"name": "Card 1", "front": "{{Headword}}", "back": "{{Definition}}",}
        ],
    )

    VerbCard = proto.Model[WordData](
        MODELS["VERB"],
        "ru-verb",
        guid=priority([use_cached_guid(anki, MODELS["VERB"]), default_guid], ""),
        fields=[],
        templates=[
            {"name": "Card 1", "front": "{{Headword}}", "back": "{{Definition}}",}
        ],
    )

    deck = proto.Deck[WordData](
        DECKS["MAIN"],
        "Russian",
        subdecks=[
            proto.Deck[WordData](DECKS["ADJECTIVES"], "Adjectives", WordCard, adjectives),
            proto.Deck[WordData](DECKS["NOUNS"], "Nouns", WordCard, nouns),
            proto.Deck[WordData](DECKS["VERBS"], "Verbs", WordCard, verbs),
        ],
    )

    if ph.target("ru.apkg"):
        deck.build("ru.apkg")

    if ph.target("ru-nomedia.apkg"):
        deck.build("ru-nomedia.apkg", include_media=False)


if __name__ == "__main__":

    generate_main()
    # generate_alphabets()

ph = PathHelper("ru")

rd = RussianDeck(sqlite("proto.db"), ph.ifile("rus_eng_full2.dct"))

bd = Builder("ru", rd)

# Check if we need stuff
if bd.needAnyData():

    print("Filtering out paired verbs.")
    info = WikiInfo(sqlite("proto.db"), ph.ifile("rus_eng_full2.dct"))
    skip = {}

    if not os.path.exists("verbskip.js"):
        for verb in Progress(filtered["Verbs"]):
            if verb in skip:
                continue
            pair = info.getAspectualPair(verb)
            if pair:
                skip[pair] = 1

        with open("verbskip.js", "w") as f:
            f.write(json.dumps(skip))
    else:
        with open("verbskip.js", "r") as f:
            skip = json.loads(f.read())

    filtered["Verbs"] = [
        verb for verb in filtered["Verbs"] if not verb in skip and verb
    ]

    for key in filtered:
        bd.bindDeckData("Russian::%s" % key, filtered[key])

bd.build(ignoreMedia=False)
