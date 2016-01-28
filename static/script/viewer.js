var app = angular.module('viewerApp', []);

app.controller('viewerCtrl', function($scope, $http, $window) {

  $scope.mangas = [];
  $scope.manga_selected = "None";

  $scope.getMyCtrlScope = function() {
    return $scope;
  }

  $scope.$watch('manga_selected', function() {
    if($scope.manga_selected != "None") {
      angular.forEach($scope.mangas, function(value, number) {
        if(value["name"] != $scope.manga_selected){
          value["hidden"] = true;
        }
      });
    }
    $scope.manga_selected = "None";
  });

  $scope.show_all_manga = function() {
    angular.forEach($scope.mangas, function(value, number) {
      value["hidden"] = false;
    });
  };

  //init
  (function() {
    successCallback = function(rep){
      $scope.mangas = rep.data["mangas"]
      angular.forEach($scope.mangas, function(value, number) {
        value["hidden"] = false;
      });
    };
    errorCallback = function(rep){
      if(rep.status == 401) {
        $window.location.href = '/login';
      }
      else {
        console.log(rep)
      }
    };
    $http.get("/mangas", { params: { date: Date.now()}}).then(successCallback, errorCallback);
  })();

});
