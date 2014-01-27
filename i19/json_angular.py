#!/usr/bin/env python

"""
Merge gettext json files into angular module "i19dict"
used for pre-loading languages
"""

import sys
import os

from distutils.cmd import Command

JS_TEMPLATE = u"""angular.module('i19catalog', []).factory('i19catalog', function() { 
var d = {};
%sreturn d;
});"""



class json_angular(Command):

    description = 'Embed message JSON files in AngularJS module'
    user_options = [
        ('domain=', 'D',
         "domain of PO file (default 'messages')"),
        ('directory=', 'd',
         'path to base directory containing the catalogs'),
        ('locales=', 'l',
         'comma-separated list of locales to include (default: all)'),
        ('json-url=', 'j',
         "base url for loading non-included locales' json file"),
    ]

    def initialize_options(self):
        self.domain = 'messages'
        self.directory = 'locale'
        self.locales = None
        self.json_url = ''

    def finalize_options(self):
        if self.locales:
            self.locales = self.locales.split(',')

    def run(self):
        out = []
        for locale in sorted(os.listdir(self.directory)):
            file_name = os.path.join(
                self.directory,
                locale,
                'LC_MESSAGES',
                self.domain + '.json'
            )
            if os.path.exists(file_name):
                if ((self.locales is None) or (locale in self.locales)):
                    print "Include:", file_name
                    out.append(file(file_name).read())
                else:
                    url = "%s%s/%s.json" % (self.json_url, locale, self.domain,)
                    print "URL:", url
                    out.append('{"%s": "%s"}' % (locale, url,))

        json = [u'angular.extend(d, %s);\n' % o for o in out]
        out_name = os.path.join(self.directory, self.domain + '.js')
        with file(out_name, 'w') as outf:
            outf.write(JS_TEMPLATE % (''.join(json)))
            print "Wrote AngularJS module i19catalog to", out_name

