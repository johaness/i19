/**
 * @fileoverview Angular module i19
 *
 */

angular.module('i19', ['i19dict']).
factory('$i19', ['$rootScope', 'i19dict', '$http', '$q',
    function($scope, i19dict, $http, $q) {
    /**
     * @name $i19
     * @class $i19 service
     */

    /**
     * Current language
     * @private
     */
    var language = 'en';

    /**
     * Translation function
     * @function
     * @name $i19.call
     * @param {string} input i18n ID of translation string
     * @returns {string} translation for i18n ID in current language
     * @example $i19('Welcome') == 'Willkommen'
     */
    function translate(input) {
        var output = i19dict[language][input];

        if (!output)
            console.warn('i19: ' + language + ' missing "' + input + '"');

        return output || input;
    }

    /**
     * Get current language
     * @function
     * @name $i19.get_lang
     * @returns {string} 2 character locale id
     */
    translate.get_lang = function() {
        return language;
    }

    /**
     * Set current language
     * @function
     * @name $i19.set_lang
     * @param {string} new_lang locale id for new language
     * @returns {deferred}
     * @example $i19.set_lang('de')
     */
    translate.set_lang = function (new_lang) {
        var def = $q.defer();

        function do_set_lang() {
            language = new_lang;
            $scope.$broadcast('language_changed');
            def.resolve(language);
        }

        if (angular.isUndefined(i19dict[new_lang])) {
            console.error("No i19 data for language " + new_lang);
            def.reject();
        }
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
        else do_set_lang();
        return def;
    }

    return translate;
}]).

/**
 * @name i19
 * @class i19 directive
 * @description Internationalization of HTML tag *content*
 */
directive('i19', ['$i19', '$compile', function($i19, $compile) {
    return {
        priority: 99,
        compile: function(elem, attrs, transclude) {
            var i19id = attrs.i19 || elem.html().trim();
            elem.html();
            return function($scope) {
                function re_compile() {
                    elem.html($i19(i19id));
                    $compile(elem.contents())($scope)
                }
                $scope.$on('language_changed', re_compile);
                re_compile();
            }
        }
   }
}]).

/**
 * @name i19a
 * @class i19a directive
 * @description Internationalization of HTML *attributes*
 * @example
 * &lt;img alt="Image description" i19a="alt"&gt;
 * @example
 * &lt;img alt="Image description" i19a="alt img-desc-signup"&gt;
 */
directive('i19a', ['$i19', '$interpolate', function($i19, $interpolate) {
    return {
        priority: 98,
        compile: function(elem, attrs, transclude) {
            var attr_names = {},
                watchers = [];
            // build mapping {attribute_name: i19id}
            angular.forEach(attrs.i19a.split(','), function(attspec) {
                var spec = attspec.trim().split(' '),
                    aname = spec[0].trim();
                this[aname] = (spec[1] || '').trim() || attrs[aname];
                elem.attr(aname, '');
            }, attr_names);
            return function link($scope) {
                function re_compile() {
                    watchers.map(function(unregister) { unregister(); });
                    angular.forEach(attr_names, function(i19id, aname) {
                        var translated = $i19(i19id),
                            transpolated = $interpolate(translated, true);
                        if (transpolated) {
                            // if the translation string is interpolated,
                            // we need to watch for changes
                            watchers.push(
                                $scope.$watch(transpolated, function(nv) {
                                    elem.attr(aname, nv);
                                }));
                        } else {
                            elem.attr(aname, translated);
                        }
                    }, watchers);
                }
                $scope.$on('language_changed', re_compile);
                re_compile();
            }
        }
    }
}]).

/**
 * @name i19i
 * @class i19i directive
 * @description Marker for HTML elements inside i19 directives
 * @example
 * &lt;i19="outer"&gt; Click &lt;a i19i="link"&gt; here &lt;/a&gt; to continue &lt;/i19&gt;
 */
directive('i19n', ['$i19', '$compile', function($i19, $compile) {
    return {
        priority: 100,
        compile: function(elem, attrs, transclude) {
            // the i19 directive on the outer element will load this HTML from
            // the translation string later, so we remove it here to prevent any binding
            // to happen in the meantime
            elem.remove();
        }
    }
}]);
