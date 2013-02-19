i19 - i18n tool chain for angularjs

Roughly consists of:

* Angular directives that mark translation strings
* Angular service that provides the translation engine
* Python translation string extractor, dumps to gettext format
* (then use the massive tool chain that is available to handle gettext stuff, pybabel is a good friend)
* gettext PO file to JSON converter

Some other features:
* the JSON files with the translation strings can be included in a JS file to be available from the start (think default language) or loaded upon language change (secondary languages)
* app remains single page - no reload upon language change
* full support for angular expressions in i18n strings, eg. <b>You have {{credits}} EUR left</b>, with the usual automatic bindings and updates; same for attributes
* i18n strings can also contain full html ala <a ng-click='do()'>foo</a> (I dont think you would want to use this in general, but experience shows that it might come in handy eventually..)
* supports i18n IDs (named translation strings), reverts to default string as ID
* in case this turns out to be a bad idea way in the future, the syntax is easily converted into Chameleon style i18n attributes for offline processing

All in all the above is a pretty standard gettext workflow. The resulting POs are fully GNU gettext compatible, so you can load them e.g. into Google Translation toolkit and work in a nice UI with automatic translation features and thesaurus and what not.
On the other hand, this remains an inline i18n solution, so the HTML inevitably gets more cluttered. I tried to keep it minimal though, some samples:

<i19>Tag only</i19>

<div i19>Attribute marker</div>

<div i19="product-view-headline">With explicit i18n IDs</div>

<img alt="Translated Attribute" i19a="alt" />

<img alt="Translated too" i19a="alt with-i18n-id" />

<img alt="Translated" title="Translated too" i19a="alt, title with-another-i18n-id" />

alert($i19("Hello World"));

A code base should probably stick to one of the two styles -- explicit i18n id or not --
I personally prefer using them for explicitness and as a helper for translators.

This is working quite nicely in a minimal demo now, next up are:
* Speed measurements
* JS string extractor
* Build system (currently: Makefile; babel provides setuptools extensions - not sure if desirable)
* Tests
* Documentation

