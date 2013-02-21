i19
===

a i18n tool chain for angularjs

Requirements
------------

pybabel, beautifulsoup4

Components
----------

Angular module:
 * Directives that mark translation strings
 * Service that provides the translation engine

Translation toolchain:
 * String extractor, dumps to gettext POT format (Python)
 * gettext PO file to JSON converter (Python)

Features
--------

Some other features:
 * the JSON files with the translation strings can be included in a JS file to be available from the start (think default language) or loaded upon language change (secondary languages)
 * app remains single page - no reload upon language change
 * full support for angular expressions in i18n strings, eg. <b>You have {{credits}} EUR left</b>, with the usual automatic bindings and updates; same for attributes
 * i18n strings can also contain full html ala <a ng-click='do()'>foo</a> (I dont think you would want to use this in general, but experience shows that it might come in handy eventually..)
 * supports i18n IDs (named translation strings), reverts to default string as ID
 * in case this turns out to be a bad idea way in the future, the syntax is easily converted into Chameleon style i18n attributes for offline processing

All in all the above is a pretty standard gettext workflow. The resulting POs are fully GNU gettext compatible, so you can load them e.g. into Google Translation toolkit and work in a nice UI with automatic translation features and thesaurus and what not.
On the other hand, this remains an inline i18n solution, so the HTML inevitably gets more cluttered.

Usage
-----

Examples
--------

.. highlight:: html

Usage Examples::

    <i19>Tag only</i19>

    <div i19>Attribute marker</div>

    <div i19="product-view-headline">With explicit i18n IDs</div>

    <img alt="Translated Attribute" i19a="alt" />

    <img alt="Translated too" i19a="alt with-i18n-id" />

    <img alt="Translated" title="Translated too" i19a="alt, title with-another-i18n-id" />


.. highlight:: javascript

From Javascript::

    alert($i19("Hello World"));

A code base should probably stick to one of the two styles -- explicit i18n id or not --
I personally prefer using them for explicitness and as a helper for translators.

TODO
----

 * Features:

   * Error checking upon JSON compile:

     * translated string should use same variables as original string
     * same for nested expressions

   * Eval angular pluralization support vs rolling our own
   * JS string extractor
   * Handle multiple occurences of the same i19n ID

 * Speed measurements
 * Build system (currently: Makefile; babel provides setuptools extensions - not sure if desirable)
 * Tests
 * Documentation

