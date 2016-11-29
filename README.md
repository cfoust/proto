PROTO is a python toolkit for generating Anki flashcard decks
=============================================================

Dependencies: beautifulsoup4 requests peewee progressbar pattern

[Anki](http://ankisrs.net/) is an application for PC, Mac, iOS and
(unofficially) Android that exposes language learners to new words
and ensures they don't forget old ones by showing them only the 
words they are about to forget each day. The application does not
come with any flashcards built-in, which means that users either have
to make decks by hand through a complicated process or download
the creations of other users.

Proto is a toolkit that generates Anki-compatible flash card decks
given a list of words as input. Anki interprets cards as a list of
fields, each of which corresponds to some information about the
given word like the definition, pronunciation, et cetera.

Proto generates cards by combining modules that pull data from a wide
range of sources: 
* [Forvo](forvo.com): Native speaker audio for words in many world languages.
* [Wiktionary](https://www.wiktionary.org/): Crowdsourced definitions.
* SDictionary: Legacy dictionary format with extensive records for some
languages.
* [WordReference[(http://www.wordreference.com/)
* [EDict](http://www.edrdg.org/jmdict/edict.html): Extensive Japanese-English 
dictionary.
* And many others.

Right now there is support for:
* Russian
* Japanese

But Spanish, French, and German are in the works.
