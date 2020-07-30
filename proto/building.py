"""
Common utilities for building decks.
"""
import os
from typing import List, Dict, Optional, Set


def get_mod_time(path: str) -> Optional[float]:
    if not os.path.exists(path):
        return None

    return os.path.getmtime(path)


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
        self._inputs: Set[str] = set()

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

        result = os.path.join(self._input, path)
        self._inputs.add(result)
        return result

    def output(self, path: str) -> str:
        """
        Returns the relative path of the requested output file.
        """
        return os.path.join(self._output, path)

    def target(self, path: str) -> bool:
        """
        If the target is older than the newest input, return true.
        """
        inputs = filter(
            lambda x: x is not None, [get_mod_time(x) for x in self._inputs]
        )

        if not inputs:
            return False

        max_input: Optional[float] = max(inputs)
        target: Optional[float] = get_mod_time(self.output(path))

        # I don't think this can happen but okay
        if not max_input or not target:
            return False

        return target < max_input


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
