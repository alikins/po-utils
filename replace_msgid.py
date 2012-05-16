#!/usr/bin/python

import sys
import polib


msg=sys.argv[1]
newmsg=sys.argv[2]
pofiles=sys.argv[3:]

for pofile in pofiles:
    print "updating %s" % pofile
    po = polib.pofile(pofile)
    pe = po.find(msg)
    pe.msgid = newmsg
    po.save()


