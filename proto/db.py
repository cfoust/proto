from peewee import *

def sqlite(path):
	return SqliteDatabase(path)