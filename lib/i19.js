angular.module('i19', ['i19dict']).
factory('$i19', ['$rootScope', 'i19dict', '$http', function($scope, i19dict, $http) {
    // Manage current language
    var language = 'en';

    function get_lang() {
        return language;
    }

    function set_lang(new_lang) {
        function do_set_lang() {
            language = new_lang;
            $scope.$broadcast('language_changed');
        }
        new_lang = new_lang.slice(0, 2);
        if (angular.isUndefined(i19dict[new_lang]))
            console.error("No i19 data for language " + new_lang);
        else if (angular.isString(i19dict[new_lang]))
            $http.get(i19dict[new_lang]).success(function(d) {
                i19dict[new_lang] = d[new_lang];
                do_set_lang();
            });
        else
            do_set_lang();
    }

    // Translation function
    function translate(input) {
        var output = i19dict[language][input];

        if (!output)
            console.error('i19: ' + language + ' missing "' + input + '"');

        return output || input;
    }

    translate.get_lang = get_lang;
    translate.set_lang = set_lang;

    return translate;
}]).
directive('i19', ['$i19', '$compile', function($i19, $compile) {
    return {
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
directive('i19a', ['$i19', '$interpolate', function($i19, $interpolate) {
    return {
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
}]);
