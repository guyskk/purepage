var app = angular.module('plunker', []);
app.controller('MainCtrl', function($scope, $http) {
	$http.get('/api/article/list')
		.success(function(response) {
		    $scope.data = response;
		})
});