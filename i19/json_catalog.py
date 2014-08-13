#!/usr/bin/env python

"""
Compile gettext po file into json
"""

import sys
import os
import json
import re

try:
    from cPickle import load  # Python 2.x
except ImportError:
    from pickle import load  # Python 3.x

from logging import warn, info, getLogger

from distutils.cmd import Command
from babel.messages.pofile import read_po


# Match variables or nested i19-name tags
# TODO broader regex
# ${match}
INCLUDES = re.compile('(\$\{[\w\-\.]*\})')
# {{match}}
ANGULAR = re.compile('(\{\{[\w\-\.\(\)]*\}\})')

# Match plural number and expression in PO header
PLURAL_FORMS = re.compile('^nplurals=(\d+); plural=(.*)$')



class json_catalog(Command):

    description = 'convert message catalogs to JSON files'
    user_options = [
        ('domain=', 'D',
         "domain of PO file (default 'messages')"),
        ('directory=', 'd',
         'path to base directory containing the catalogs'),
        ('expr-cache=', 'e',
         'name of expression cache file'),
    ]

    def initialize_options(self):
        self.domain = 'messages'
        self.directory = 'locale'
        self.expr_cache = None

    def finalize_options(self):
        if not self.expr_cache:
            self.expr_cache = os.path.join(
                    self.directory, self.domain, '.pot.i19n')

    def run(self):
        for locale in os.listdir(self.directory):
            file_name = os.path.join(
                self.directory,
                locale,
                'LC_MESSAGES',
                self.domain + '.po'
            )
            if os.path.exists(file_name):
                json_name = file_name[:-2] + 'json'
                write_json(file_name, locale, self.expr_cache, json_name)



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

def validate_message(translation, original, msgid, skip_missing_var=False):
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
            (skip_missing_var or _contains(org_var, tr_var,
                    "Translation misses variable %s in %r", msgid)) and
            _contains(tr_inc, org_inc,
                    "Translation introduces reference %s in %r", msgid) and
            _contains(tr_var, org_var,
                    "Translation introduces variable %s in %r", msgid)
            )


def catalog2dict(catalog, cache_file):
    """Convert PO catalog to dict suitable for JSON serialization"""
    __stats = [0, 0]

    with file(cache_file) as caf:
        include_cache, original_strings = load(caf)

    def single(msg_id, msg_str, skip_check=False):
        """Convert a single message string"""
        __stats[0] += 1
        default = original_strings.get(msg_id, None)
        if msg_str and (default is None or
                validate_message(msg_str, default[1], msg_id, skip_check)):
            __stats[1] += 1
            return add_includes(msg_str, include_cache)
        else:
            return ''

    def entry(message):
        """Convert a single message ID"""
        if not message.pluralizable:
            return message.id, single(message.id, message.string)
        else:
            return message.id[0], \
                    [single(message.id[0], mstr, i == 0)
                            for i, mstr in enumerate(message.string)]

    return dict([entry(msg) for msg in catalog]), __stats[0], __stats[1]


def extract_plural_func(catalog):
    """Extract nplurals and plural from catalog's Plural-Forms header"""
    forms = dict(catalog.mime_headers)['Plural-Forms']
    return PLURAL_FORMS.match(forms).groups()


def write_json(po_file, locale, cache_file, jo_file):
    """
      SOURCE po file
      LOCALE locale identifier
      CACHE cache file created by i19extract.py
      OUTPUT JSON file
    """
    getLogger().name = po_file
    getLogger().level = 0

    with file(po_file) as pof:
        catalog = read_po(pof, locale)

    messages, total, translated = catalog2dict(list(catalog)[1:], cache_file)

    info("%s: %d of %d (%d unique) translated (%d%%)",
            jo_file, translated, total,
            len(messages), 100.0 * translated / total,)

    messages['__pluralization_count__'], messages['__pluralization_expr__'] = \
            extract_plural_func(catalog)

    with file(jo_file, 'w') as json_file:
        json.dump({locale: messages}, json_file)

