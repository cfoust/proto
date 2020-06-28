from peewee import SqliteDatabase


def sqlite(path):
    return SqliteDatabase(path)
