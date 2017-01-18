import os, sys
from setuptools import setup, find_packages

setup(
    name="proto",
    version="1.0.0",
    author="Caleb Foust",
    author_email="cfoust@sqweebloid.com",
    description=("Library offering handy abstractions"
                 " to build Anki decks programmatically."),
    install_requires=[
        "beautifulsoup4",
        "requests",
        "peewee",
        "progressbar2",
        "anki"
    ],
    dependency_links=['http://github.com/cfoust/anki/tarball/master#egg=anki-2.1.0a8'],
    packages=find_packages()
)
