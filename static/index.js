var myApp = angular.module('MangaApp', ['ngRoute', 'loginApp', 'viewerApp']);

myApp.factory('User', function() {
  var user;
  return {
    setUser: function(user) {
      this.user = user;
    },
    getUser : function() {
      return this.user;
    }
  }
});

myApp.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/login',
  {
    controller: 'loginCtrl',
    templateUrl: '/static/login/login.html'
  }).when('/view',
  {
    controller: 'viewerCtrl',
    templateUrl: '/static/viewer/viewer.html'
  }).otherwise(
  {
    redirectTo: '/login'
  });
}]);
