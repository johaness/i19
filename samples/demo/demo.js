angular.module('demo', ['i19']).
controller('ctl', ['$scope', '$i19', function($scope, $i19) {
    $scope.$i19 = $i19;
    $scope.count = 1;
    $scope.ts = function() { return new Date(); };
    $scope.modal = function() { alert($i19("Well done")); };
}]);
