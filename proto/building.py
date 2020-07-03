"""
Common utilities for building decks.
"""
import os
from typing import List
from peewee import SqliteDatabase

class PathHelper(object):
    """
    Simple pathing logic.
    """

    def __init__(self, code: str) -> None:
        """Takes in a ISO-639-1 language code and creates
           the directory structure."""

        self.code = code

        self._output = os.path.join("output", code)
        self._input = os.path.join("input", code)
        self._db = os.path.join(self._input, code, ".db")

        for folder in [self._input, self._output]:
            if not os.path.exists(folder):
                os.makedirs(folder)

    @property
    def db(self) -> str:
        return self._db


    def input(self, path: str) -> str:
        """
        Returns the relative path of the requested input file. For example,
        if you pass in 'asd.txt' and your language code is 'de', you would get
        back 'input/de/asd.txt' as long as the file exists.
        """

        return os.path.join(self._input, path)


    def output(self, path: str) -> str:
        """
        Returns the relative path of the requested output file.
        """
        return os.path.join(self._output, path)


def get_file_lines(path: str) -> List[str]:
    """
    Get the lines of a file with the given filename as a list of strings.
    """
    if not os.path.isfile(path):
        return []

    op = open(path, "r")
    lines = op.readlines()
    op.close()
    return [x.rstrip() for x in lines]


def sqlite(path):
    return SqliteDatabase(path)
