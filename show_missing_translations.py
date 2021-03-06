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

from collections import defaultdict
from optparse import OptionParser


def default_factory_list():
    return defaultdict(list)


def default_factory_default_factory():
    return defaultdict(default_factory_list)


def line_no_cmp(a, b):
    return int(a) - int(b)


def main():
    parser = OptionParser()
    parser.add_option("-l", "--locale", dest="locales",
                      action="append",
                      help="which locales/langs to check")
    parser.add_option("-p", "--po-dir", dest="podir",
                      help="where to find po files")

    options, args = parser.parse_args()

    po_path = "po/"
    if options.podir:
        po_path = options.podir

    po_files = glob.glob("%s/*.po" % po_path)

    pos = defaultdict(default_factory_default_factory)
    for po_file in po_files:
        print po_file
        p = polib.pofile(po_file)
        for entry in p.untranslated_entries():
            for line in entry.occurrences:
                entry_abs_path = os.path.abspath("%s/%s" % (po_path, line[0]))
                pos[entry_abs_path][line[1]]['langs'].append(os.path.basename(po_file))
                pos[entry_abs_path][line[1]]['msgid'] = entry.msgid

        for entry in p.fuzzy_entries():
            for line in entry.occurrences:
                entry_abs_path = os.path.abspath("%s/%s" % (po_path, line[0]))
                pos[entry_abs_path][line[1]]['langs'].append(os.path.basename(po_file))
                pos[entry_abs_path][line[1]]['msgid'] = entry.msgid

    source_files = args

    if not source_files:
        source_files = pos.keys()

    full_path = []
    for source_file in source_files:
        full_path.append(os.path.abspath(source_file))
    source_files = full_path

    for source_file in source_files:
        abs_path = source_file
        if abs_path in pos:
            warning_lines = pos[abs_path]
            warning_lines_keys = warning_lines.keys()

            warning_lines_keys.sort(cmp=line_no_cmp)
            for warning_line_key in warning_lines_keys:
                warning_line = warning_lines[warning_line_key]
                # each line_no
                print "%s:%s %s %s" % (abs_path,
                                       warning_line_key,
                                        "(%s)" % ','.join(warning_line['langs']),
                                       warning_line['msgid'])

if __name__ == "__main__":
    main()
