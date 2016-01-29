angular.module('loginApp', [])
.service('loginService', function($http, $location, User) {
  this.login = function(username, password, errorCallback) {
    data = {
      login : username,
      pwd : password
    }
    success = function(rep){
      User.setUser(rep.data['name']);
      $location.path('/view')
    };
    error = function(rep){
      errorCallback();
    };
    $http.post("/login", data).then(success, error);
  };

  this.logout = function() {
    successCallback = function(rep){
    User.setUser("");
    $location.path('/login')
    };
    errorCallback = function(rep){
      console.log("error" + rep)
    };
    $http.get("/logout").then(successCallback, errorCallback);
  };
})

.controller('loginCtrl', function($scope, $rootScope, $http, $location, $route, User, loginService) {
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
    loginService.login($scope.login, $scope.password, function() {
      $scope.showError = {'visibility':'visible'}
      $scope.login = ""
      $scope.password = ""
    })
  };
});
