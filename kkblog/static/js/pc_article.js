var app = angular.module('plunker', []);
app.controller('MainCtrl', function($scope, $http) {
	$http.get('/api/article/list',{
		"git_username":localStorage.git_username
	})
		.success(function(response) {
		    $scope.data = response;
		})
});