var app = angular.module('viewerApp', []);

app.controller('viewerCtrl', function($scope, $http, $window) {

  $scope.logout = function(){
    successCallback = function(rep){
      console.log("success");
      console.log(rep)
      console.log("redirect to /")
      $window.location.href = '/';
    };
    errorCallback = function(rep){
      console.log("success");
      console.log(rep)
    };
    $http.get("/logout").then(successCallback, errorCallback);
  };
});
