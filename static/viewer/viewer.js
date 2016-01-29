angular.module('viewerApp', ['loginApp'])
.controller('viewerCtrl', function($scope, $rootScope, $http, $location, User, loginService) {

  $scope.mangas = [];
  $scope.manga_selected = "None";
  $scope.chapters = [];
  $scope.userName = "";

  $scope.init = function() {
    $scope.userName =  User.getUser();
    console.log("user is " + $scope.userName)
  }

  $scope.getMyCtrlScope = function() {
    return $scope;
  }

  $scope.$watch('manga_selected', function() {
    if($scope.manga_selected != "None") {
      angular.forEach($scope.mangas, function(value, number) {
        if(value["name"] != $scope.manga_selected){
          value["show"] = false;
        } else {
          //manga selected
          debut = value["start"];
          end = value["stop"];
          for(i = debut; i <= end; i++) {
            $scope.chapters.push(i);
          }
        }
      });
    }
  });

  $scope.home = function() {
    angular.forEach($scope.mangas, function(value, number) {
      if( value["show"] == false) {
        value["show"] = true;
      }
    });
    $scope.manga_selected = "None";
    $scope.chapters = []
  };

  $scope.logout = function() {
    loginService.logout();
    /*successCallback = function(rep){
      User.setUser("");
      $location.path('/login')
    };
    errorCallback = function(rep){
      console.log("error" + rep)
    };
    $http.get("/logout").then(successCallback, errorCallback);*/
  };

  //init
  (function() {
    successCallback = function(rep){
      $scope.mangas = rep.data["mangas"]
      angular.forEach($scope.mangas, function(value, number) {
        value["show"] = true;
      });
    };
    errorCallback = function(rep){
      if(rep.status == 401) {
        $location.path('/login');
      }
      else {
        console.log(rep)
      }
    };
    $http.get("/mangas", { params: { date: Date.now()}}).then(successCallback, errorCallback);
  })();
});
