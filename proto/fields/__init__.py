from .basic import *

try:
	import requests, bs4
	from .conwiktion import *
	from .forvocate import *
except:
	print('Either "requests" or "bs4", or both, are not installed. Cannot load special fields.')
