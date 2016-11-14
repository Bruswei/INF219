angular.module('mountainApp', [])

.controller('listController', ['$scope', '$http', function($scope, $http) {
    $scope.mountains = []

    $scope.label = function(m) {
        if (m.height < 1000) {
            return "label-primary"
        } else if (m.height < 2500) {
            return "label-info"
        } else if (m.height < 4000) {
            return "label-success"
        } else if (m.height < 5000) {
            return "label-warning"
        } else {
            return "label-danger"
        }
    }

    $http.get('/mountain_list.json')
        .success(function(data, status, headers, config) {
            $scope.mountains = data;
            console.log(data);
        })
        .error(function(data, status, headers, config) {
            console.log(status);
        });
}]);
