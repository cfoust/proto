"""Grabs a definition from an SDict dictionary. This was a dictionary used by
a single program in the 90s and early aughts for translation and such. Lots of
old dictionary files for them exist on the Internet, and some of these files are
far better than any online resources. Russian is a good example of this. """

import sdictviewer.formats.dct.sdict as sdict
import sdictviewer.dictutil
from ...fields import FieldType

class SDictField(FieldType):
    def __init__(self,dict):
        self.dict = sdict.SDictionary(dict)
        self.dict.load()

    def pull(self,word):
        """The code that looks through the dictionary is a little bit odd, but
           the efficiency is definitely better than O(n). Just looks strange."""
        for item in self.dict.get_word_list_iter( word ):
            try:
                if word == str( item ):
                    instance, definition = item.read_articles()[0]
                    return definition
            except:
                continue
        return None
