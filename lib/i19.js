angular.module('i19', ['i19dict']).
factory('$i19', ['$rootScope', 'i19dict', function($scope, i19dict) {
    // get / set current language
    var language = 'en';

    this.get_lang = function() { return language; }

    this.set_lang = function(new_lang) {
        new_lang = new_lang.slice(0, 2);
        if (i19dict[new_lang] === undefined) {
            console.error("No i19 data for language " + new_lang);
        } else {
            language = new_lang;
            $scope.$broadcast('language_changed');
        }
    }

    // translation
    this.translate = function translate(input, scope, is_repeat) {

        var output = i19dict[language][input];

        if (!output)
            console.error('i19: ' + language + ' missing "' + input + '"');

        return output || input;
    }
    return this;
}]).
directive('i19', ['$i19', function($i19) {
    return function($scope, elem, attrs, transclude) {
        var i19id = attrs.i19 || elem.html().trim();

        function match(s) { return (s || '').match(/{{.*}}/g); };

        function translate(is_first) {
            var res = $i19.translate(i19id, $scope);
            angular.forEach(match(res), function(m) {
                var inner = m.slice(2, -2);
                res = res.replace(m, $scope.$eval(inner) || '');
                if (is_first)
                    $scope.$watch(inner, function(nv, ov) {
                        if (nv !== ov) translate(false);
                    });
            });
            elem.html(res);
        }

        $scope.$on('language_changed', translate);

        translate(true);
    }
}]);
