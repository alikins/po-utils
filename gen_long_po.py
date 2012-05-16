#!/usr/bin/python

import polib
import sys

path = sys.argv[1]
pofile = polib.pofile(path)

for entry in pofile:
    orig = entry.msgstr
    new = orig + "\n"*40
#    new = "_"
    entry.msgstr = new

pofile.save(path)
