#!/usr/bin/env python

"""
Extract i19 messages from HTML, dump gettext pot file to stdout

Usage: i19extract source0.html source1.html > domain.pot
"""

import sys
from HTMLParser import HTMLParser
import time

# from pygettext
pot_header = '''\
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR ORGANIZATION
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\\n"
"POT-Creation-Date: %s\\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\\n"
"Language-Team: LANGUAGE <LL@li.org>\\n"
"MIME-Version: 1.0\\n"
"Content-Type: text/plain; charset=utf-8\\n"
"Content-Transfer-Encoding: ENCODING\\n"
"Generated-By: i19extract.py 0.1\\n"

'''



class i19Parser(HTMLParser):
    def __init__(self, filename):
        HTMLParser.__init__(self)
        self._i19 = None
        self._strs = dict()
        self._fn = filename
        with file(filename) as f:
            self.feed(f.read())

    def handle_starttag(self, tag, attrs):
        attrdict = dict(attrs)

        # handle i19 tag for translating the inner HTML
        if tag == 'i19':
            self._i19 = ''
        elif not 'i19' in attrdict:
            self._i19 = None
        else:
            self._i19 = attrdict.get('i19') or ''

        # handle i19a tag for translating attributes
        if not 'i19a' in attrdict:
            return
        for attribute in attrdict.get('i19a').split(','):
            spec = attribute.strip().split(' ')
            value = attrdict[spec[0]]
            if len(spec) == 1: # no translation id given
                spec.append(value)
            self._strs[spec[1]] = ("%s:%d" % (self._fn, self.lineno,), value)


    def handle_endtag(self, tag):
        self._i19 = None

    def handle_data(self, data):
        if self._i19 is None:
            return
        data = data.strip().replace('\n', '\\n')
        self._strs[self._i19 or data] = ("%s:%d" % (self._fn, self.lineno,), data)



def main():
    assert len(sys.argv) > 1, "Usage: i19extract source0 source1 .."

    strs = dict()
    for src_file in sys.argv[1:]:
        parser = i19Parser(src_file)
        strs.update(parser._strs.items())

    print pot_header % (time.strftime('%Y-%m-%d %H:%M+0000'),)

    for k, v in strs.items():
        print "#. Default:", v[1]
        print "#:", v[0]
        print 'msgid "%s"' % k
        print 'msgstr ""'
        print

if __name__ == '__main__':
    main()
