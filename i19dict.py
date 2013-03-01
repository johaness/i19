#!/usr/bin/env python

"""
Merge gettext json files into angular module "i19dict"
used for pre-loading languages
"""

import sys

JS_TEMPLATE = u"""angular.module('i19dict', []).factory('i19dict', function() { 
var d = {}; %s return d;
});"""


def main():
    """
    Usage: i19dict target.js source0.json source1.json ..
    """
    assert len(sys.argv) > 2, main.__doc__

    json = [u'angular.extend(d, %s);' % (file(fn).read(),)
            for fn in sys.argv[2:]]

    with file(sys.argv[1], 'w') as outf:
        outf.write(JS_TEMPLATE % (''.join(json)))


if __name__ == '__main__':
    main()
