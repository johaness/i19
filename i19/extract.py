#!/usr/bin/env python

"""
Extract i19 messages from HTML, write gettext pot file and include cache
"""

import sys
import os
from HTMLParser import HTMLParser
import time
from cPickle import dump, load
import re

# List of void HTML elements (ie without end tag)
VOID_TAGS = (
    # HTML4
    # http://www.w3.org/TR/html4/index/elements.html
    'area', 'base', 'basefont', 'br', 'col', 'frame', 'hr', 'img',
    'input', 'isindex', 'link', 'meta', 'param',
    # New in HTML5
    # http://www.w3.org/TR/html-markup/syntax.html#void-element
    'command', 'embed', 'keygen', 'source', 'track', 'wbr',
)



def fmttag(tag, attr, exclude=()):
    """
    Unparse HTML element ``tag`` with attributes ``attr`` into a string
    Skip attributes in ``exclude``
    """
    return "<%s>" % (" ".join([tag] +
        ['%s="%s"' % (k, v) for k, v in attr if not k in exclude]),)


def sanitize(i19id):
    """
    Filter i18n IDs to contain only alphanumeric characters and ``-_``
    """
    e19id = re.sub(r'\\.', '', i19id)
    return "".join(c for c in e19id if c.isalnum() or c in "-_")


class i19Parser(HTMLParser):
    """
    Parse HTML and extract i19, i19-attr, and i19-name strings
    """
    def __init__(self, filename):
        HTMLParser.__init__(self)
        # stack of i18n IDs
        self._i19 = []
        # tag nesting level counter
        self._nest = 0
        # id, nesting level, and raw html of current include directive
        self._include = ['', 0, '']
        # collect {i18n ID: translation strings}
        self.strs, self.includes = dict(), dict()

        self.feed(filename.read())

    def handle_starttag(self, tag, attrs):
        if not tag in VOID_TAGS:
            self._nest += 1
        attrdict = dict(attrs)

        # handle i19-name attribute for nested translations
        if 'i19-name' in attrdict:
            i19id = "${" + attrdict['i19-name'] + "}"
            self._i19[-1][1] += i19id
            self._include = [i19id, self._nest, '']

        # record raw html for i19 string if closest parent is not i19-name
        if self._i19 and self._i19[-1][2] >= self._include[1]:
            self._i19[-1][1] += fmttag(tag, attrs)

        # record raw html for i19-name directive
        if self._include[1]:
            self._include[2] += fmttag(tag, attrs, ('i19-name',))

        # handle i19 tag/attribute for translating the inner HTML
        if tag == 'i19':
            self._i19.append(['', '', self._nest])
        elif 'i19' in attrdict:
            self._i19.append([attrdict.get('i19') or '', '', self._nest])
        elif 'data-i19' in attrdict:
            self._i19.append([attrdict.get('data-i19') or '', '', self._nest])

        # handle i19-attr attribute for translating attributes
        trans_attr = []
        if 'i19-attr' in attrdict:
            trans_attr = attrdict.get('i19-attr').split(',')
        elif 'data-i19attr' in attrdict:
            trans_attr = attrdict.get('data-i19attr').split(',')

        for attribute in trans_attr:
            spec = attribute.strip().split(' ')
            if not spec[0] in attrdict:
                raise RuntimeError(
                        "Cannot find attribute %r on <%s> in :%s" %
                        (spec[0], tag, self.lineno,))
            value = attrdict[spec[0]]
            if len(spec) == 1: # no translation id given
                spec.append(value)
            self.strs[spec[1]] = (
                self.lineno, value, '<%s %s>' % (tag, spec[0])
            )


    def handle_endtag(self, tag):
        if not tag in VOID_TAGS:
            self._nest -= 1

        if not self._i19:
            return

        # store raw html
        if self._include[1]:
            self._include[2] += "</" + tag + ">"

        # i19 directive not closed yet
        if self._i19[-1][2] <= self._nest:
            self._i19[-1][1] += "</" + tag + ">"
            return

        i19id, data, _ = self._i19.pop()

        if self._i19 and self._include[0]:
            # documentation for nested i19 tags
            doc = "Referenced in %r as %s" % \
                    (self._i19[-1][0], self._include[0],)
        else:
            doc = ''

        # end of include directive
        if self._include[1] >= self._nest:
            inid, _, raw = self._include
            self.includes[inid] = raw
            self._include = ['', 0, '']

        data = data.strip().replace('\n', '\\n')
        self.strs[(i19id or sanitize(data))] = (self.lineno, data, doc)

    def handle_data(self, data):
        if not self._i19:
            return
        self._i19[-1][1] += data
        if self._include[1]:
            self._include[2] += data



def extract(fileobj, keywords, comment_tags, options):
    """
    Invoked by Babel per file
    """
    parser = i19Parser(fileobj)
    for i19id, dt in parser.strs.items():
        if i19id.endswith(')'):
            yield (dt[0], 'ngettext', (i19id, i19id,), [u"Default: %s" % dt[1], dt[2]])
        else:
            yield (dt[0], None, i19id,  [u"Default: %s" % dt[1], dt[2]])
    if os.path.isfile(options['expr_cache']):
        with file(options['expr_cache']) as i19n:
            inc, strs = load(i19n)
    else:
        inc, strs = {}, {}
    inc.update(parser.includes)
    strs.update(parser.strs)
    with file(options['expr_cache'], 'wb') as i19n:
        dump((inc, strs,), i19n)

