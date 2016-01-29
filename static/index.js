var myApp = angular.module('MangaApp', ['ngRoute', 'ngCookies', 'loginApp', 'viewerApp']);

myApp.factory('User', function($cookies) {
  var user;
  var factory = {};
  factory.setUser = function(user) {
    this.user = user;
    $cookies.put('username', user);
  };
  factory.getUser = function() {
    return this.user;
  };
  factory.setUser($cookies.get('username'));
  console.log('cookie retrieve, name is '+factory.getUser());
  return factory;
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
