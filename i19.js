/**
 * @fileoverview Angular module i19
 * @name i19
 *
 */

angular.module('i19', ['i19dict']).
/**
 * @class $i19 service
 * @name i19.$i19
 * @requires i19dict
 * @returns {function} i19.$i19.translate
 */
factory('$i19', ['$rootScope', 'i19dict', '$http', '$q',
    function($scope, i19dict, $http, $q) {

    /**
     * @private
     * @description Current language
     */
    var language = 'en';

    /**
     * @private
     * @description Convert an amount into an index into the pluralization list
     */
    function count2plural(n) {
        return 0 + eval(i19dict[language].__pluralization_expr__);
    }

    /**
     * @name i19.$i19.translate
     * @class
     *
     * @description
     * Translation function
     *
     * @param {string} input i18n ID of translation string
     * @returns {string} translation for i18n ID in current language
     *
     * @example $i19('Welcome') == 'Willkommen'
     */
    function translate(input, plural) {
        var output = i19dict[language][input];

        if (!angular.isUndefined(plural))
            output = output[count2plural(plural)];

        if (!output && translate.warn_on_missing_strings)
            console.warn('i19: ' + language + ' missing "' + input + '"');

        return output;
    }
    /**
     * @property {bool} i19.$i19.translate.warn_on_missing_strings
     *
     * @description emit console warning for each missing translation string
     */
    translate.warn_on_missing_strings = true;
    /**
     * @property {bool} i19.$i19.translate.fallback_default
     *
     * @description return default string in case no translation
     *              is available; if false, return i18n ID
     */
    translate.fallback_default = true;

    /**
     * @name i19.$i19.translate._extract_plural
     * @function
     *
     * @description
     */
    translate._extract_plural = function(i19id) {
        var pl_start = i19id.indexOf('(') + 1;
        if (pl_start > 0)
            return i19id.slice(pl_start, -1);
    }

    /**
     * @name i19.$i19.translate._sanitize
     * @function
     *
     * @description convert default translation string into acceptable i19 ID
     */
    translate._sanitize = function(default_value) {
        return default_value.replace(/[^A-Za-z0-9\-_]/gi,'');
    }

    /**
     * @name i19.$i19.translate._parse_i19attr
     * @function
     *
     * @param {string} i19attr raw i19-attr value
     * @param {object} attrs element attributes
     * @param {string} initialize all internationalized attributes with this
     *                 value. omit to leave untouched.
     * @returns {object} mapping {attribute_name:
     *                   [i19id, pluralization expr, default value]}
     */
    translate._parse_i19attr = function(i19attr, elem, attrs, init) {
        var attr_map = {};
        angular.forEach(i19attr.split(','), function(attspec) {
            var spec = attspec.trim().split(' '),
                aname = spec[0].trim(),
                i19id = (spec[1] || '').trim(),
                plural = translate._extract_plural(i19id);
            attrs = attrs || {}; // no defaults if attr_map missing
            this[aname] = [i19id || translate._sanitize(attrs[aname]),
                plural, attrs[aname]];
            init && elem.attr(aname, init);
        }, attr_map);
        return attr_map;
    }

    /**
     * @name i19.$i19.translate.get_lang
     * @function
     *
     * @description
     * Get current language
     *
     * @returns {string} 2 character locale id
     */
    translate.get_lang = function() {
        return language;
    }

    /**
     * @name i19.$i19.translate.set_lang
     * @function
     *
     * @description
     * Set current language
     *
     * @param {string} new_lang locale id for new language
     * @returns {deferred}
     *
     * @example $i19.set_lang('de')
     */
    translate.set_lang = function (new_lang) {
        var def = $q.defer();

        function do_set_lang() {
            language = new_lang;
            $scope.$broadcast('language_changed');
            def.resolve(language);
        }

        // invalid language
        if (angular.isUndefined(i19dict[new_lang])) {
            console.error("No i19 data for language " + new_lang);
            def.reject();
        }
        // language data available through separate JSON file
        else if (angular.isString(i19dict[new_lang])) {
            $http.get(i19dict[new_lang]).
                success(function(d) {
                    i19dict[new_lang] = d[new_lang];
                    do_set_lang();
                }).
                error(function() {
                    def.reject();
                });
        }
        // language data already available
        else do_set_lang();
        return def;
    }

    return translate;
}]).

/**
 * @name i19.i19
 * @class i19 directive
 *
 * @description
 * Internationalization of HTML tag *content*
 */
directive('i19', ['$i19', '$compile', function($i19, $compile) {
    return {
        priority: 99,
        compile: function(elem, attrs, transclude) {
            var i19id = attrs.i19 || $i19._sanitize(elem.html().trim()),
                plural = $i19._extract_plural(attrs.i19 || ''),
                deflt = elem.html(),
                watcher;
            return function($scope, elem) {
                function re_compile() {
                    if (plural) {
                        watcher && watcher();
                        watcher = $scope.$watch(plural, function(count) {
                            elem.html($i19(i19id, count) ||
                                ($i19.fallback_default ? deflt : i19id));
                            $compile(elem.contents())($scope)
                        });
                    } else {
                        elem.html($i19(i19id) ||
                            ($i19.fallback_default ? deflt : i19id));
                        $compile(elem.contents())($scope)
                    }
                }
                $scope.$on('language_changed', re_compile);
                re_compile();
            }
        }
   }
}]).

/**
 * @name i19.i19-attr
 * @class i19-attr directive
 *
 * @description Internationalization of HTML *attributes*
 *
 * @example
 * &lt;img alt="Image description" i19-attr="alt"&gt;
 *
 * @example
 * &lt;img alt="Image description" i19-attr="alt img-desc-signup"&gt;
 */
directive('i19Attr', ['$i19', '$interpolate', function($i19, $interpolate) {
    return {
        restrict: 'A',
        priority: 98,
        compile: function(elem, attrs, transclude) {
            var attr_map = $i19._parse_i19attr(attrs.i19Attr, elem, attrs, '');
            return function link($scope, elem) {
                var watcher = {};
                // Translate and interpolate one attribute
                function transpolate(id_pl, aname) {
                    var i19id = id_pl[0],
                        plural = id_pl[1],
                        deflt = id_pl[2],
                        translated = $i19(i19id,
                                plural && $scope.$eval(plural)) ||
                            ($i19.fallback_default ? deflt : i19id);
                        transpolated = $interpolate(translated, true);
                    // re-initialize watchers after every language or
                    // pluralization change to deal with changing variable
                    // names between translation strings
                    (watcher[aname] || []).map(function(unregister) { unregister(); });
                    watcher[aname] = [];
                    if (plural) {
                        watcher[aname].push(
                            $scope.$watch(plural, function(nv, ov) {
                                if (nv !== ov) transpolate(id_pl, aname);
                            }));
                    }
                    if (transpolated) {
                        // if the translation string is interpolated,
                        // we need to watch for changes
                        watcher[aname].push(
                            $scope.$watch(transpolated, function(nv) {
                                elem.attr(aname, nv);
                            }));
                    } else {
                        elem.attr(aname, translated);
                    }
                }
                // render all attributes
                function re_compile() {
                    angular.forEach(attr_map, transpolate);
                }
                $scope.$on('language_changed', re_compile);
                re_compile();
            }
        }
    }
}]).

/**
 * @name i19.i19-name
 * @class i19-name directive
 *
 * @description
 * Marker for HTML elements inside i19 directives
 *
 * @example
 * &lt;i19="outer"&gt; Click &lt;a i19-name="link"&gt; here &lt;/a&gt; to continue &lt;/i19&gt;
 */
directive('i19-name', ['$i19', '$compile', function($i19, $compile) {
    return {
        restrict: 'A',
        priority: 100,
        compile: function(elem, attrs, transclude) {
            // the i19 directive on the outer element will load this HTML from
            // the translation string later, so we remove it here to prevent any binding
            // to happen in the meantime
            elem.remove();
        }
    }
}]);
