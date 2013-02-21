i19
===

an internationalization tool chain for angularjs

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

 1. Annotate HTML (see Examples below), include ``lib/i19n.js``
 2. Run extraction (see ``demo/Makefile``)
 3. Edit translation strings (see ``demo/locales/en/LC_MESSAGES/demo.po``)
 4. Compile JSON language file (eg ``demo/locales/en.json``) and
    JavaScript preloader ``i19dict.js``
 5. Switch languages on the fly by calling ``$i19.set_lang('de')``


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


Examples
--------

.. highlight:: html

Anonymous tag::

    <i19>Tag only</i19>

===============  ===========================
i19 ID           Default
===============  ===========================
Tag only         Tag only
===============  ===========================

Anonymous tag marked by attribute::

    <div i19>Attribute</div>

===============  ===========================
i19 ID           Default
===============  ===========================
Attribute        Attribute
===============  ===========================

Named tag::

    <div i19="product-view-h">With explicit i18n IDs</div>

===============  ===========================
i19 ID           Default
===============  ===========================
product-view-h   With explicit i18n IDs
===============  ===========================

Anonymous attributes::

    <img alt="Translated" i19a="alt" />

===============  ===========================
i19 ID           Default
===============  ===========================
Translated       Translated
===============  ===========================

Named attributes::

    <img alt="Translated too" i19a="alt with-i18n-id" />

===============  ===========================
i19 ID           Default
===============  ===========================
with-i18n-id     Translated too
===============  ===========================

Multiple attributes::

    <img alt="Translated" title="Translated too" i19a="alt, title with-another-id" />

===============  ===========================
i19 ID           Default
===============  ===========================
Translated       Translated
with-another-id  Translated too
===============  ===========================

Embedded HTML elements::

    <p i19="para">Text with a
      <button i19i="button" i19="button-label">named chunk of html</button>
      inside.
    </p>

===============  =============================
i19 ID           Default
===============  =============================
para             Text with a ${button} inside.
button-label     named chunk of html
===============  =============================


.. highlight:: javascript

From Javascript::

    alert($i19("Hello World"));

A code base should probably stick to one of the two styles -- explicit i18n id or not --
I personally prefer using them for explicitness and as a helper for translators.


Requirements
------------

pybabel, make


TODO
----

 * Speed measurements
 * Features:

   * Handle multiple occurences of the same i19n ID
   * JS string extractor
   * Eval angular pluralization support vs rolling our own
   * Manhole for live updates of translation files

 * Tests
 * Build system (currently: Makefile; babel provides setuptools extensions - not sure if desirable)
 * Documentation

