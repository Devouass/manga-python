var myApp = angular.module('MangaApp', ['ngRoute', 'loginApp']);

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
    templateUrl: '/login.html',
    controller: 'loginCtrl'
  }).otherwise(
  {
    redirectTo: '/login'
  });
}]);
