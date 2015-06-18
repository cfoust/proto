from basic import CacheableFieldType
import requests, os, urllib, urllib2, string, base64, hashlib, time, random, shutil
from bs4 import BeautifulSoup as soup

def get_data_from_url(url_in):
	return requests.get(url_in).text

def get_soup_from_url(url_in):
	return soup(get_data_from_url(url_in))

class ForvoField(CacheableFieldType):
	db_name = "forvocate"
	anki_name = "Audio"
	html = """%s"""

	def __init__(self,pathToDb,languageCode,
				 storagePath = None,
				 outputPath = None,
				 throttle=True,
				 soundCap=1,
				 randomSound=False):
		self.db_name = self.db_name + '-' + languageCode
		CacheableFieldType.__init__(self,pathToDb)

		self.code = languageCode
		
		self.throttle = throttle
		self.soundCap = soundCap
		self.randomSound = randomSound
		if not storagePath:
			self.storage_path = 'forvocate/' + languageCode + '/'
		else:
			self.storage_path = storagePath

		if not os.path.exists(self.storage_path):
			os.makedirs(self.storage_path)

		if not outputPath:
			self.output_path = 'media/' + languageCode + '/'
		else:
			self.output_path = outputPath

		if not os.path.exists(self.output_path):
			os.makedirs(self.output_path)
		

	def pull(self,word):
		result = CacheableFieldType.pull(self,word)

		if not result:
			return '' # It doesn't matter if this field has nothing
		try:
			word = word.encode('utf-8')
		except:
			pass

		# Generates the resulting file paths based on the number of sounds we stored.
		results = [hashlib.md5(word).hexdigest() 
		          + str(x) + '.mp3' 
		          for x in range(int(result))]

		if len(results) == 0:
			return ''

		if self.randomSound:
			choice = random.choice(results)
		else:
			choice = results[0]

		if not os.path.exists(self.output_path + choice):
			shutil.copyfile(self.storage_path + choice,self.output_path + choice)

		return '[sound:%s]' % choice 

	def generate(self,word):
		downloads_list = []

		try:
			word = word.encode('utf-8')
		except:
			pass

		u_word = urllib.quote(word)

		language = "en"
		target = self.code
		url = 'http://www.forvo.com/word/%s/#%s' % (u_word,target)

		word_soup = get_soup_from_url(url)

		languages = word_soup.findAll(attrs={'class': 'word'})

		for language in languages:
			abbr = language.findAll('abbr')[0].contents[0]
			if abbr == target:
				a_list = language.findAll('a')
				for a in a_list:
					try:
						href = a['onclick']
					except KeyError:
						continue
					# construct the url again
					parts = string.split(href,",")
					if "Play" in parts[0]:
						mp3_64 = parts[1][1:-1]
						mp3_url = 'http://audio.forvo.com:80/mp3/{0}'.format(base64.b64decode(mp3_64))
						downloads_list.append(mp3_url)
					else:
						continue

		# Clear out old downloads
		hashed = hashlib.md5(word).hexdigest()
		index = 0
		while os.path.isfile(self.storage_path + hashed + str(index) + '.mp3'):
			os.remove(self.storage_path + hashed + str(index) + '.mp3')
			index += 1

		# Download the new sounds
		for i,url in enumerate(downloads_list):
			if i == self.soundCap:
				break
			r = requests.get(url)
			with open(self.storage_path + hashed + str(i) + '.mp3','wb') as code:
				code.write(r.content)
			if self.throttle:
				time.sleep(1.0)

		numSounds = min(len(downloads_list),self.soundCap)
		if numSounds == 0:
			return None
		else:
			return str(numSounds)