from wikiinfo import *
from ...fields import FieldType

class RussianVerbStressField(FieldType):
	def __init__(self,pathToDb,sdictPath):
		self.info = WikiInfo(pathToDb,sdictPath)

	def pull(self,word):
		return self.info.getStress(word)