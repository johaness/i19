i19
===

Internationalization tool chain for AngularJS

Components
----------

Angular module:
 * Directives that mark translation strings
 * Service that provides the translation engine

Translation toolchain:
 * String extractor, dumps to gettext POT format (Python)
 * gettext PO file to JSON converter (Python)

Workflow
--------

 1. Annotate HTML (see Examples below), include ``lib/i19.js``
 2. Run extraction (see Usage below)
 3. Edit translation strings (see ``demo/locales/en/LC_MESSAGES/demo.po``)
 4. Compile JSON language file (eg ``demo/locales/en.json``) and
    JavaScript pre-loader
 5. Use the ``$i19`` angular service and switch languages on the fly by calling ``$i19.set_lang('de')``


Features
--------

Some other features:
 * the JSON files with the translation strings can be included in a JS file to be available from the start (think default language) or loaded upon language change (secondary languages)
 * app remains single page - no reload upon language change
 * full support for angular expressions in i18n strings, eg. ``<b>You have {{credits}} EUR left</b>``, with the usual automatic bindings and updates; same for attributes
 * error checking upon compilation: introduction of new ``{{scope}}`` or ``<i1i="template">`` references
 * i18n strings can also contain full html ala ``<a ng-click='do()'>foo</a>`` (I dont think you would want to use this in general, but experience shows that it might come in handy eventually..)
 * supports i18n IDs (named translation strings), reverts to default string as ID
 * in case this turns out to be a bad idea way in the future, the syntax is easily converted into Chameleon style i18n attributes for offline processing

All in all the above is a pretty standard gettext workflow. The resulting POs are fully GNU gettext compatible, so you can load them e.g. into Google Translation toolkit and work in a nice UI with automatic translation features and thesaurus and what not.
On the other hand, this remains an inline i18n solution, so the HTML inevitably gets more cluttered.


Translation Examples
--------------------

.. highlight:: html

The following examples demonstrate usage of the various ``i19-*`` attributes
and show the resulting translation data.

To translate the *content* of an HTML element, either use the ``i19`` tag::

    <i19>Tag only</i19>

===============  ===========================
i19 ID           Default
===============  ===========================
Tag only         Tag only
===============  ===========================

or the ``i19`` attribute::

    <div i19>Attribute</div>

===============  ===========================
i19 ID           Default
===============  ===========================
Attribute        Attribute
===============  ===========================

To help translators we strongly suggest giving each translation string a name ("i19 ID") 
to establish context::

    <div i19="product-view-h">With explicit i18n IDs</div>

===============  ===========================
i19 ID           Default
===============  ===========================
product-view-h   With explicit i18n IDs
===============  ===========================

To translate *attributes* of HTML nodes, use the ``i19-attr`` tag::

    <img alt="Translated" i19-attr="alt" />

===============  ===========================
i19 ID           Default
===============  ===========================
Translated       Translated
===============  ===========================

Again, you should provide a name for the string::

    <img alt="Translated too" i19-attr="alt portrait-alt" />

===============  ===========================
i19 ID           Default
===============  ===========================
portrait-alt     Translated too
===============  ===========================

Multiple attributes can be translated by separating them with commas.
You can mix between explicit and implicit i19 IDs::

    <img alt="Translated" title="Translated too" i19-attr="alt, title with-another-id" />

===============  ===========================
i19 ID           Default
===============  ===========================
Translated       Translated
with-another-id  Translated too
===============  ===========================

Sometimes you need to translate elements that are contained in other elements
that need to be translated as well. Consider this example::

    <p>Click <a href="..">here</a> to continue</p>

While i19 allows you to just include the ``<a href..``, it is 
less error-prone if the translator does not have to deal with
HTML at all.
Ideally, she should translate two strings separately:

 * the "here" from the link caption, and
 * the surrounding string, preferably with a placeholder: "Click ${placeholder} to continue"

i19 supports this functionality via the ``i19-name`` attribute::

    <p i19="outer">Click 
        <a i19-name="link-to-next" i19="link-caption">here</a>
        to continue
    </p>


===============  =============================
i19 ID           Default
===============  =============================
outer            Click ${placeholder} to continue
link-caption     here
===============  =============================

The translation notes for "link-caption" will also include a reference to the
source string: "Referenced in 'outer' as ${placeholder}"


.. highlight:: javascript

Finally, the translation engine can be accessed programmatically from Javascript::

    alert($i19("Hello World"));


Configuration
-----

.. highlight:: makefile

Create a new ``Makefile`` for your project::

    # languages to pre-load by including in JavaScript
    LANGUAGES_INCLUDE=en

    # other languages available as JSON for delayed loading
    LANGUAGES_OTHER=de

    # translation domain
    DOMAIN=my_app

    # locale directory, will create one sub-directory per language
    LOCALES=locale/

    # HTML sources
    HTML=*.html

    # Output: JavaScript file for pre-loading translation strings
    I19JS=locale/i19dict.js

    include common.mk


.. highlight:: shell

Initialize the translation file structure once::

    make -Ipath/to/i19py init

Usage
-----

Extract strings from source, merge with update existing translations,
compile JavaScript and JSON output::

    make -Ipath/to/i19py

Instead of providing the path to i19py on the command line you can also
change the ``include common.mk`` line in the Makefile to contain the full path.


Requirements
------------

pybabel, make


Future Features
---------------

  * Handle multiple occurences of the same translation ID

    * List all filename:lineno
    * Warn if default strings vary

  * JS string extractor

    * Check if pybabel parser can be used

  * Attribute/Tag name converter for Chameloen to verify fall back

  * Eval angular pluralization support vs rolling our own

    * Possible syntax: Parameter to i18n ID e.g. ``<i19="id(number)">..``

  * Manhole for live updates of translation files

    * Allow translators to see the live app with their own tranlation strings


TODO
----

 * Speed measurements
 * Unittests
 * Integration tests: HTML source files w/ corner cases
 * Build system (currently: Makefile; babel provides setuptools extensions - not sure if desirable)
 * Documentation

