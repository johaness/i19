angular.module('demo', ['i19']).
controller('ctl', ['$scope', '$i19', function($scope, $i19) {
    $scope.$i19 = $i19;
    $scope.ts = function() { return new Date(); };
}]);
