#!/usr/bin/env python

"""
Compile gettext po file into json

Usage: i19json source.po locale output.json

Where `locale` is a 2 character locale identifier
"""

import sys
import simplejson

from babel.messages.pofile import read_po

def main():
    po_file, locale, jo_file = sys.argv[1:4]

    with file(po_file) as f:
        catalog = list(read_po(f, locale))[1:]

    messages = dict((message.id, message.string)
            for message in catalog
            if message.string)

    print "%s: %d of %d translated (%d%%)" % \
            (jo_file, len(messages), len(catalog), 
                    100.0 * len(messages) / len(catalog),)

    with file(jo_file, 'w') as jo:
        simplejson.dump({locale: messages}, jo)


if __name__ == '__main__':
    main()
