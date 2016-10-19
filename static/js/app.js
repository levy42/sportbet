'use strict';

/* App */

var app = angular.module('App', ['AppServices', 'Auth'])
    .config(['$routeProvider', '$locationProvider',
        function ($routeProvider, $locationProvider) {
            $routeProvider
                .when('/', {
                    templateUrl: 'static/partials/index.html',
                    controller: HomeController
                })
                .when('/login', {
                    templateUrl: 'static/partials/login.html',
                    controller: AuthController
                })
                .when('/register', {
                    templateUrl: 'static/partials/register.html',
                    controller: AuthController
                })
                .when('/logout', {
                    templateUrl: 'static/partials/logout.html',
                    controller: AuthController
                })
                .otherwise({
                    redirectTo: '/'
                })
            ;

            $locationProvider.html5Mode(true);
        }]);
