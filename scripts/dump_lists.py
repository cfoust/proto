"""

"""
import sys

from proto.anki import AnkiDeck, split_fields

if __name__ == "__main__":
    args = sys.argv

    if len(args) != 2:
        print("wat are you doing")

    file = args[1]
    anki = AnkiDeck(file)

    decks = anki.get_decks()
    ids = {
        "%s.csv" % v["name"].translate(str.maketrans("", "", ":")): int(k)
        for k, v in decks.items()
    }

    for deck in ids:
        _id = ids[deck]

        results = anki.db.execute(
            """
            SELECT nid from cards WHERE did = ?
            """,
            (_id,),
        ).fetchall()

        rows = []

        # Gotta go in and grab from notes
        for result in results:
            row = anki.db.execute(
                """
                SELECT flds from notes WHERE id = ?
                """,
                (result[0],),
            ).fetchone()

            if row is None:
                continue

            rows.append(split_fields(row[0])[0])

        with open(deck, "w") as f:
            f.write("\n".join(rows))
