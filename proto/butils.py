import os
from proto.exporters import APKGExporter
from progressbar import Bar, ProgressBar, Percentage, ETA



def Progress(data):
	end = len(data)
	pbar = ProgressBar(widgets=[Percentage(), Bar(), ETA()], maxval=len(data)).start()
	for i,datum in enumerate(data):
		yield datum
		pbar.update(i + 1)
	pbar.finish()


class PathHelper:
	db = 'proto.db'
	def __init__(self,code):
		self.output = 'output/%s/' % code
		self.input = 'input/%s/' % code
		self.media = 'media/%s/' % code
		self.code = code

	def ifile(self,fn):
		# The path of the file
		p = self.input + fn

		if os.path.exists(p):
			return p
		else:
			raise Exception('File %s not found in input directory.' % fn)

	def ofile(self,fn):
		return self.output + fn

	def mfile(self,fn):
		# The path of the file
		p = self.media + fn

		if os.path.exists(p):
			return p
		else:
			raise Exception('File %s not found in media directory.' % fn)

	def apkgExport(self,deck, ignoreMedia = False):
		deckPath = self.output + self.code + '.apkg'

		APKGExporter.export(deck,deckPath,self.output,self.media,ignoreMedia = ignoreMedia)

	def neededFiles(self,deck):
		def _neededFiles(pname,deck):
			needed = []
			if deck.cardType != None:
				csvfile = "%s-%s.csv" % (pname,deck.csvname)

				if not os.path.exists(self.ofile(csvfile)):
					needed.append(csvfile)

			for subdeck in deck.subdecks:
				needed += _neededFiles(deck.csvname,subdeck)

			return needed

		return _neededFiles('',deck)

def fileLines(fn):
	if os.path.isfile(fn):
		op = open(fn, 'r')
		lines = op.readlines()
		op.close()
		return [x.rstrip() for x in lines]
	else:
		return []

def loadTemplate(tname):
	p = 'templates/%s' % tname

	if os.path.exists(p):
		return open(p,'r').read()
	else:
		raise Exception('Template %s not found in template directory.' % fn)
	

def applyDefaultTemplate(deck, recursive = True):
	if deck.cardType != None:
		deck.cardType._css = loadTemplate('proto.css')
		deck.cardType._js = loadTemplate('proto.js')
		deck.cardType._bheader = loadTemplate('proto.header.html')
		deck.cardType._bfooter = loadTemplate('proto.footer.html')

	if not recursive:
		return

	for sd in deck.subdecks:
		applyDefaultTemplate(sd)