#!/usr/bin/env python

"""
Compile gettext po file into json

Usage: i19json SOURCE LOCALE CACHE OUTPUT

SOURCE po file
LOCALE locale identifier
CACHE cache file created by i19extract.py
OUTPUT JSON file

"""

import sys
import simplejson
from cPickle import load
import re
from logging import warn

from babel.messages.pofile import read_po


INCLUDES = re.compile('(\$\{\w*\})')


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


def main():
    po_file, locale, cache_file, jo_file = sys.argv[1:5]

    with file(po_file) as pof:
        catalog = list(read_po(pof, locale))[1:]

    with file(cache_file) as caf:
        include_cache = load(caf)

    messages = dict((message.id, add_includes(message.string, include_cache))
            for message in catalog
            if message.string)

    print "%s: %d of %d translated (%d%%)" % \
            (jo_file, len(messages), len(catalog), 
                    100.0 * len(messages) / len(catalog),)

    with file(jo_file, 'w') as json:
        simplejson.dump({locale: messages}, json)


if __name__ == '__main__':
    main()
