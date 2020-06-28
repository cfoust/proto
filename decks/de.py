from proto.butils import *
from proto.builder import *

from proto.languages.de import GermanDeck
from proto.exporters import CSVExporter, APKGExporter

from pattern.de import parse, split
from pattern.de import attributive, predicative, singularize

ph = PathHelper("de")

gd = GermanDeck(ph.db)

# Apply Templates
applyDefaultTemplate(gd)
vbs = gd.subDeckByName("Verbs").cardType
# Sets up the custom stuff for verbs
vbs._js = open(ph.ifile("verb.js"), "r").read()
vbs.fields[3].html = open(ph.ifile("verb.html"), "r").read()

bd = Builder("de", gd)

# Check if we need stuff

if bd.needAnyData():

    # Bind data if we do
    words = get_file_lines(ph.ifile("words.txt"))

    filtered = {"Adjectives": [], "Nouns": [], "Verbs": []}

    print("Filtering out frequencies.")
    for word in Progress(words):
        if len(word.split(" ")) > 1:
            continue

        info = parse(word).split("/")
        if info[1] == "JJ":
            filtered["Adjectives"].append(predicative(word))
        elif info[1] == "NN":
            filtered["Nouns"].append(singularize(word.decode("utf-8")))
        elif info[1] == "VB" and word[-1] == "n":
            filtered["Verbs"].append(word)

    print("Filtering out duplicates.")
    for key in ["Adjectives", "Nouns", "Verbs"]:
        old = filtered[key]
        filtered[key] = []
        for word in old:
            if not word in filtered[key]:
                filtered[key].append(word)

    for key in filtered:
        bd.bindDeckData("German::%s" % key, filtered[key])

bd.build(ignoreMedia=True)
