#!/usr/bin/python

import os
import sys
import locale 
import gettext


sys.path.append("/usr/share/rhsm")
from subscription_manager.i18n import configure_i18n
configure_i18n(with_glade=True)
_ = lambda x: gettext.ldgettext("rhsm", x)

test_locales = [
        # as_IN is kind of busted in RHEL6, and seemingly
        # very busted in 14
        #"as_IN",   # Assamese
        "bn_IN",  # Bengali
        "de_DE",  # German
        "es_ES",  # Spanish
        "en_US",  # english us
        "fr_FR",  # French
        "gu_IN",  # Gujarati
        "hi_IN",  # Hindi
        "it_IT",  # Italian
        "ja_JP",  # Japanese
        "kn_IN",  # Kannada
        "ml_IN",  # Malayalam
        "mr_IN",  # Marathi
        "or_IN",  # Oriya
        "pa_IN",  # Punjabi
        # "ne_IN",  # Nepali
        #"se_IN", # Sinhala
        #"br_IN", # Maithili
        "pt_BR",  # Portugese
        "ru_RU",  # Russian
        #"si_LK",   # Sri Lankan
        "ta_IN",  # Tamil
        "te_IN",  # telgu
        "zh_CN",  # Chinese Simplified
        "zh_TW",  # Chinese Traditional
        "ko_KR"]  # korean

msgids=sys.argv[1:]

for lang in test_locales:
    os.environ['LANG'] = "%s.UTF8" % lang
    locale.setlocale(locale.LC_ALL, '')
    for msgid in msgids:
        print "%s: %s" % (lang, _(msgid))
