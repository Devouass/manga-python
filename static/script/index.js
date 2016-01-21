var app = angular.module('loginApp', []);

app.controller('loginCtrl', function($scope, $http) {
  $scope.login = "";
  $scope.password = "";
  $scope.isDisable = function() {
    if($scope.login == "" || $scope.password == "") {
      return true;
    }
    return false;
  };
  $scope.save = function(){
    data = {
      login : $scope.login,
      pwd : $scope.password
    }
    successCallback = function(rep){
      console.log("success");
      console.log(rep)
    };

    errorCallback = function(rep){
      console.log("error");
      console.log(rep)
    };
    $http.post("/login", data).then(successCallback, errorCallback);
  };
});
