import proto

from proto.building import PathHelper, get_file_lines

from decks.ja.jmdict import JMDictGetter, JMReadingGetter

def generate_main():
    """
    Generate the primary Japanese deck.
    """
    ph = PathHelper("ja")

    WordCard = proto.Model(
        1527532200,
        "ja-word",
        guid=lambda data: data[0],
        fields=[
            proto.Field("Headword", lambda data: data[0],),
            proto.Field("Reading", JMReadingGetter(ph.input("JmdictFurigana.txt"))),
            proto.Field("Definition", JMDictGetter(ph.input("JMdict_e"))),
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
            Deck("Adjectives", WordCard, adjectives),
            Deck("Nouns", WordCard, nouns),
            Deck("Verbs", WordCard, verbs),
        ],
    )

    if ph.target('ja.apkg'): deck.build('ja.apkg')
    if ph.target('ja-nomedia.apkg'): deck.build('ja-nomedia.apkg', media=False)


def generate_alphabets():
    ph = PathHelper("ja")

    WordCard = proto.Model(
        1116319754,
        "ja-stroke",
        guid=lambda data: data[0],
        fields=[
            proto.Field("Headword", lambda data: data[0],),
            proto.Field("Reading", JMReadingGetter(ph.input("JmdictFurigana.txt"))),
            proto.Field("Definition", JMDictGetter(ph.input("JMdict_e"))),
            # The part of speech
            proto.Field("POS", lambda data: data[-1],),
        ],
        templates=[{"name": "Card 1", "front": "", "back": "",}],
    )
    pass


if __name__ == '__main__':
    generate_main()
    generate_alphabets()
