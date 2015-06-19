import sdictviewer.formats.dct.sdict as sdict
import sdictviewer.dictutil
from ...fields import FieldType

class SDictField(FieldType):
    def __init__(self,dict):
        self.dict = sdict.SDictionary(dict)
        self.dict.load()

    def pull(self,word):
        found = False
        for item in self.dict.get_word_list_iter( word ):
            try:
                if word == str( item ):
                    instance, definition = item.read_articles()[0]
                    return definition
            except:
                continue
        return None
