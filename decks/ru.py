from proto.db import *
from proto.builder import *

from proto.languages.ru import RussianDeck
from proto.languages.ru.wikiinfo import WikiInfo

import json, os

ph = PathHelper("ru")

rd = RussianDeck(sqlite("proto.db"), ph.ifile("rus_eng_full2.dct"))

# Apply Templates
applyDefaultTemplate(rd)
vbs = rd.subDeckByName("Verbs").cardType
# Sets up the custom stuff for verbs
vbs._js = open(ph.ifile("verb.js"), "r").read()

bd = Builder("ru", rd)


# Check if we need stuff

if bd.needAnyData():

    words = fileLines(ph.ifile("lemma.num"))

    filtered = {"Adjectives": [], "Nouns": [], "Verbs": []}

    print "Filtering out words."
    for word in Progress(words):
        info = word.split(" ")
        pos = info[3]
        lemma = info[2]

        if pos == "noun":
            filtered["Nouns"].append(lemma)
        elif pos == "verb":
            filtered["Verbs"].append(lemma)
        elif pos == "adj":
            filtered["Adjectives"].append(lemma)

    print "Filtering out duplicates."
    for key in ["Adjectives", "Nouns", "Verbs"]:
        old = filtered[key]
        filtered[key] = []
        for word in old:
            if not word in filtered[key] and word != None:
                filtered[key].append(word)

    print "Filtering out paired verbs."
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
