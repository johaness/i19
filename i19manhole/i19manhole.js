angular.module('i19manhole', ['i19', 'i19dict']).
factory('hotkeyregistry', ['$document', '$rootScope', function($document, $rootScope) {
    $document.bind('keydown', function(e) {
        if (e.ctrlKey && e.shiftKey && e.keyCode == 72)
            $rootScope.$apply(function(s) {
                s.$broadcast('i19manhole');
            });
    });
}]).
directive('draggable', ['$document', function($document) {
    // AngularJS example
    var startX = 0, startY = 0, x = 0, y = 0;
    return function(scope, element, attr) {
      element.bind('mousedown', function(event) {
        var tName = event.target.tagName;
        if (tName == 'INPUT' || tName == 'SELECT' || tName == 'TEXTAREA') return true;
        element.css('-webkit-user-select', 'none');
        startX = event.screenX - x;
        startY = event.screenY - y;
        $document.bind('mousemove', mousemove);
        $document.bind('mouseup', mouseup);
      });

      function mousemove(event) {
        y = event.screenY - startY;
        x = event.screenX - startX;
        element.css({
          top: y + 'px',
          left:  x + 'px'
        });
      }

      function mouseup() {
        element.css('-webkit-user-select', '');
        $document.unbind('mousemove', mousemove);
        $document.unbind('mouseup', mouseup);
      }
    }
}]).
directive('i19manhole', ['$document', '$timeout', '$i19', 'i19dict', 'hotkeyregistry', function($document, $timeout, $i19, i19dict) {
    return {
        restrict: 'E',
        templateUrl: '/i19manhole/manhole.html',
        replace: true,
        link: function(scope, elm, attrs) {
            scope.$on('i19manhole', function() {
                scope.visible = !!! scope.visible;
            });
            scope.visible = false;
            scope.edit_lang = scope.display_lang = $i19.get_lang();
            scope.edit_ids = [];
            scope.i19dict = i19dict;
            scope.isArray = angular.isArray;
            scope.$watch('display_lang', function(v) {
                if (v != $i19.get_lang()) $i19.set_lang(v);
            });
            scope.$on('language_changed', function() {
                scope.display_lang = $i19.get_lang();
            });
            function pulse(target) {
                angular.element(target).
                    css('-webkit-transition', 'box-shadow 0.5s ease-in-out').
                    css('box-shadow', '0 0 5px #4bc');
                $timeout(function() {
                    angular.element(target).css('box-shadow', ''); }, 500);
            }
            angular.forEach(i19dict, function(v, k) {
                this.unshift(k);
            }, scope.langs = []);
            $document.bind('click', function(e) {
                if (! scope.visible) return;
                var target = e.target;
                if (!e.ctrlKey || !target) return;
                while (target.parentNode) {
                    var attrs = target.getAttribute('i19-attr'),
                        i19id = target.getAttribute('i19');
                    if (attrs || i19id) break;
                    target = target.parentNode;
                }
                if (! target) return;
                scope.$apply(function(s) {
                    if (i19id)
                        s.edit_ids.push(i19id);
                    if (attrs) {
                        for (var k in $i19._parse_i19attr(attrs))
                            s.edit_ids.push(k);
                    }
                });
                pulse(target);
                e.preventDefault();
            });
        }
    };
}]).
run(['$document', '$compile', function($document, $compile) {
//    var e = angular.element('<i19manhole></i19manhole>');
//    $document.find('body').append(e);
//    $compile(e);
}]);

