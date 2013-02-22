#!/usr/bin/env python

"""
Compile gettext po file into json
"""

import sys
import json
from cPickle import load
import re
from logging import warn, info, getLogger

from babel.messages.pofile import read_po

# TODO broader regex
INCLUDES = re.compile('(\$\{[\w\-\.]*\})')
ANGULAR = re.compile('(\{\{[\w\-\.\(\)]*\}\})')


def add_includes(msgstring, cache):
    """
    Replace all ${include_name} in msgstring with respective cache[include_name]
    """
    for var in INCLUDES.findall(msgstring):
        if not var in cache:
            warn("Invalid i19i identifier: %s", var)
        else:
            msgstring = msgstring.replace(var, cache[var])
    return msgstring


def _contains(src, dst, msg, msgid):
    """
    Check if all of items in `src` are also available in `dst`
    emit warning `msg` otherwise
    Used by `validate_message`
    """
    result = True
    for val in src:
        if not val in dst:
            result = False
            warn(msg, val, msgid)
    return result

def validate_message(translation, original, msgid=''):
    """
    Warn on all newly introduced or missing variables or references in the
    translation
    """
    org_inc = INCLUDES.findall(original)
    org_var = ANGULAR.findall(original)
    tr_inc = INCLUDES.findall(translation)
    tr_var = ANGULAR.findall(translation)

    return (
            _contains(org_inc, tr_inc,
                    "Translation misses reference %s in %r", msgid) and
            _contains(org_var, tr_var,
                    "Translation misses variable %s in %r", msgid) and
            _contains(tr_inc, org_inc,
                    "Translation introduces reference %s in %r", msgid) and
            _contains(tr_var, org_var,
                    "Translation introduces variable %s in %r", msgid)
            )


def main():
    """
    Usage: i19json SOURCE LOCALE CACHE OUTPUT

      SOURCE po file
      LOCALE locale identifier
      CACHE cache file created by i19extract.py
      OUTPUT JSON file
    """
    assert len(sys.argv) == 5, main.__doc__

    po_file, locale, cache_file, jo_file = sys.argv[1:5]

    getLogger().name = po_file
    getLogger().level = 0

    with file(po_file) as pof:
        catalog = list(read_po(pof, locale))[1:]

    with file(cache_file) as caf:
        include_cache, original_strings = load(caf)

    messages = dict((message.id, add_includes(message.string, include_cache))
            for message in catalog
            if message.string and
               validate_message(message.string,
                   original_strings[message.id][1], message.id))

    info("%s: %d of %d translated (%d%%)",
            jo_file, len(messages), len(catalog), 
                    100.0 * len(messages) / len(catalog),)

    with file(jo_file, 'w') as json:
        json.dump({locale: messages}, json)


if __name__ == '__main__':
    main()
