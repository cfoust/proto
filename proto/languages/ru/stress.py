from wikiinfo import *
from ...fields import FieldType

class RussianVerbStressField(FieldType):
    def __init__(self,db,sdictPath):
        self.info = WikiInfo(db,sdictPath)

    def pull(self,word):
        return self.info.getStress(word)