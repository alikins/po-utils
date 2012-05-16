#!/usr/bin/python

# sort of kind of a translation lint
#
# require's polib from https://bitbucket.org/izi/polib/wiki/Home
#
# from top level of tree:
#    check_translations.py /path/to/source/file
#
#  Should output any untranslated or fuzzy lines from the file in a "lint" style
#
# At the moment, it just shows
import glob
import polib
import os

import sys
from collections import defaultdict

#FIXME
PO_PATH = "po/"

po_files = glob.glob("%s/*.po" % PO_PATH)

source_files = sys.argv
if len(sys.argv) < 2:
    print "usage: check_translations.py /path/to/source/file"

def default_factory_list():
    return defaultdict(list)

def default_factory_default_factory():
    return defaultdict(default_factory_list)

pos = defaultdict(default_factory_default_factory)
for po_file in po_files:
    p = polib.pofile(po_file)
    for entry in p.untranslated_entries():
        for line in entry.occurrences:
            entry_abs_path = os.path.abspath("%s/%s" % (PO_PATH, line[0]))
            pos[entry_abs_path][line[1]]['langs'].append(os.path.basename(po_file))
            pos[entry_abs_path][line[1]]['msgid'] = entry.msgid

    for entry in p.fuzzy_entries():
        for line in entry.occurrences:
            entry_abs_path = os.path.abspath("%s/%s" % (PO_PATH, line[0]))
            pos[entry_abs_path][line[1]]['langs'].append(os.path.basename(po_file))
            pos[entry_abs_path][line[1]]['msgid'] = entry.msgid

def cmp(a,b):
    return int(a) - int(b)

for source_file in source_files:
    abs_path = "%s/%s" % (os.path.abspath(os.path.curdir), source_file)
    if abs_path in pos:
        warning_lines = pos[abs_path]
        warning_lines_keys = warning_lines.keys()

        warning_lines_keys.sort(cmp=cmp)
        for warning_line_key in warning_lines_keys:
            warning_line = warning_lines[warning_line_key]
            # each line_no
            print "%s:%s %s %s" % (abs_path,
                                   warning_line_key,
                                    "(%s)" % ','.join(warning_line['langs']),
                                   warning_line['msgid'])
