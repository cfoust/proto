import json
import codecs

# Need some beautiful soup for this
from bs4 import BeautifulSoup as soup

from proto.building import get_file_lines

def parse_entry(entry_string):
    # Parse the entry from its HTML
    entrySoup = soup(entry_string, "html.parser")

    # Look for all the kanji readings
    kanji_readings = []
    for r in entrySoup.findAll("k_ele"):
        obj = {}

        # Grab the reading
        obj["reading"] = r.find("keb").contents[0]

        # Get the reading's priorities
        obj["priority"] = []
        for pri in r.findAll("ke_pri"):
            obj["priority"].append(pri.contents[0])

        # Get the kanji's information fields
        obj["info"] = []
        for pri in r.findAll("ke_inf"):
            obj["info"].append(pri.contents[0])

        kanji_readings.append(obj)

    # Look for all the kana readings
    kana_readings = []
    for r in entrySoup.findAll("r_ele"):
        obj = {}

        # Grab the reading
        obj["reading"] = r.find("reb").contents[0]

        # Get the reading's priorities
        obj["priority"] = []
        for pri in r.findAll("re_pri"):
            obj["priority"].append(pri.contents[0])

        # See whether it's restricted to a certain kanji reading
        if r.find("re_restr"):
            obj["restrict"] = r.find("re_restr").contents[0]

        # Get the reading's information fields
        obj["info"] = []
        for pri in r.findAll("re_inf"):
            obj["info"].append(pri.contents[0])

        kana_readings.append(obj)

    # Now we have to parse through and combine the readings to make the
    # ultimate list of them.
    readings = []
    # If we have no kanji readings, this just a word written in kana
    if len(kanji_readings) == 0:
        for r_read in kana_readings:

            # Calculate the reading's score, or its pertinence based on
            # the various frequency indicators jmdict provides
            score = 0
            common = ["news1", "ichi1", "gail1", "spec1"]
            lessCommon = ["news2", "ichi2", "gail2", "spec2"]
            for info in r_read["priority"]:
                if info in common:
                    score += 50
                elif info in lessCommon:
                    score += 25
                elif "nf" in info:
                    score += 50 - int(info[2:])

            reading = {
                "kanji": "",
                "kana": r_read["reading"],
                "info": r_read["info"],
                "score": score,
                "priority": r_read["priority"],
            }
            readings.append(reading)

    # Otherwise we go through and assign readings
    else:
        for k_read in kanji_readings:
            for r_read in kana_readings:
                # Deal with restricted readings
                if "restrict" in r_read and r_read["restrict"] != k_read["reading"]:
                    continue

                # Calculate the reading's score, or its pertinence based on
                # the various frequency indicators jmdict provides
                score = 0
                common = ["news1", "ichi1", "gail1", "spec1"]
                lessCommon = ["news2", "ichi2", "gail2", "spec2"]
                for info in r_read["priority"]:
                    if info in common:
                        score += 50
                    elif info in lessCommon:
                        score += 25
                    elif "nf" in info:
                        score += 50 - int(info[2:])

                reading = {
                    "kanji": k_read["reading"],
                    "kana": r_read["reading"],
                    "info": r_read["info"],
                    "score": score,
                    "priority": [],
                }

                if ";".join(k_read["priority"]) == ";".join(r_read["priority"]):
                    reading["priority"] = k_read["priority"]

                readings.append(reading)

    # Parse all of the senses
    senses = []
    for sense in entrySoup.findAll("sense"):

        # Gather the misc for the sense
        miscs = []
        for misc in sense.findAll("misc"):
            miscs.append(misc.contents[0])

        # Gather the pos for the sense
        poses = []
        for pos in sense.findAll("pos"):
            poses.append(pos.contents[0])

        # Get the glosses too
        glosses = []
        for gloss in sense.findAll("gloss"):
            glosses.append(gloss.contents[0])

        senses.append({"tags": miscs, "pos": poses, "glosses": glosses})

    # Look through and get the highest score
    maxScore = 0
    for reading in readings:
        maxScore = max(maxScore, reading["score"])

    obj = {"readings": readings, "score": maxScore, "defs": senses}
    return obj


def parse_to_file(jm_dict, out):
    # Gets the lines of the dictionary
    dictLines = get_file_lines(jm_dict)

    outFile = codecs.open(out, "w", "utf-8")

    num = 0

    index = 0
    while True:
        if index >= len(dictLines):
            break

        # Store the current line
        line = dictLines[index]

        # If it's not the start of an entry, continue
        if line != "<entry>":
            index += 1
            continue

        # Start looking one line ahead
        searchIndex = index + 1

        # Store the end index
        foundEnd = False
        endIndex = -1

        # Look for where the entry definition ends
        while True:
            if searchIndex >= len(dictLines):
                break

            searchLine = dictLines[searchIndex]

            if searchLine == "</entry>":
                endIndex = searchIndex
                foundEnd = True
                break

            searchIndex += 1

        # If we didn't find the end of the entry definition, continue.
        if not foundEnd:
            index += 1
            continue

        entry = "\n".join(dictLines[index : endIndex + 1])
        parsed = parse_entry(entry)

        outFile.write(json.dumps(parsed) + "\n")

        index += 1


class JMReadingGetter(object):
    """
    Gets readings of words from JMDict.
    """

    def __init__(self, furiFile: str):
        if not os.path.exists(furiFile):
            raise Exception("JMDict furigana file '%s' does not exist." % furiFile)

        """Load the dict csv file and parse it into our dictionaries."""
        lines = get_file_lines(furiFile)

        self.readingDict: dict[str, list[str]] = {}

        numConflicts = 0

        for line in lines:
            parts = line.split("|")
            reading = parts[0]

            if reading in self.readingDict:
                self.readingDict[reading].append(line)
                numConflicts += 1
            else:
                self.readingDict[reading] = [line]

    def get_readings(self, word):
        if word in self.readingDict:
            return self.readingDict[word]

        return []

    def run(self, data):
        defs = self.get_readings(data)

        if len(defs) == 0:
            return ""
        else:
            return json.dumps(defs)


class JMDictGetter(object):
    def __init__(self, dictFile: str):
        if not os.path.exists(dictFile):
            raise Exception("JMDict file '%s' does not exist." % dictFile)

        # Check to see whether the dictionary has been parsed and parses it
        # if it hasn't
        if not os.path.exists(dictFile + ".csv"):
            print("JMDict dictionary file has not been parsed into csv. Parsing.")
            parse_to_file(dictFile, dictFile + ".csv")
            print("Done parsing.")

        """Load the dict csv file and parse it into our dictionaries."""
        lines = get_file_lines(dictFile + ".csv")

        # Sucks to suck. We had to switch to an O(n) algorithm for dictionary
        # lookups because there's really no clean way to make it a hashmap.
        #
        # I may revisit this if it becomes too slow. Japanese is not very
        # polysemous, so we could conjure some kind of key-value lookup
        # where multiple keys point to the same value. For now, this is fine.
        self.dictionary = []

        for line in lines:
            self.dictionary.append(json.loads(line))

    def get_definitions(self, word):
        results = []

        try:
            word = word.decode("utf-8")
        except:
            pass

        for definition in self.dictionary:
            for reading in definition["readings"]:
                if word == reading["kana"] or word == reading["kanji"]:
                    results.append(definition)
                    break

        results = sorted(results, key=lambda d: d["score"], reverse=True)

        return results

    def run(self, word):
        """The code that looks through the dictionary is a little bit odd, but
        the efficiency is definitely better than O(n). Just looks strange."""
        defs = self.get_definitions(word)

        if len(defs) == 0:
            return None
        else:
            return json.dumps(defs)
