var app = angular.module('loginApp', []);
app.controller('loginCtrl', function($scope, $http, $window, User) {
  $scope.login = "";
  $scope.password = "";
  $scope.showError = {'visibility':'hidden'}
  $scope.$watch('login', function() {
    if($scope.login != ""){
      $scope.showError = {'visibility':'hidden'}
    }
  })
  $scope.$watch('password', function() {
    if($scope.password != "") {
      $scope.showError = {'visibility':'hidden'}
    }
  })
  $scope.save = function(){
    data = {
      login : $scope.login,
      pwd : $scope.password
    }
    successCallback = function(rep){
      console.log(rep);
      User.setUser($scope.login);
      console.log("user saved is "+User.getUser());
      //$window.location.href = '/view'
    };

    errorCallback = function(rep){
      $scope.showError = {'visibility':'visible'}
      $scope.login = ""
      $scope.password = ""
    };
    $http.post("/login", data).then(successCallback, errorCallback);
  };
});
