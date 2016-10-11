'use strict';

angular.module('AppServices', ['ngResource']).factory('HomeService', ["$http", function ($http) {

}]);


angular.module('Auth', ['ngResource'])
    .factory('AuthService', ["$http", function ($http) {
        return {
            login: function (username, password) {
                var data = {
                    username: username,
                    password: password
                };
                return $http.post("/auth/login", data).then(function (response) {
                    if (response.status == 200) return true;
                    else return response.data.result
                })
            },
            logout: function () {
                return $http.get("/auth/logout").then(function (response) {
                    if (response.status == 200)return true;
                    else return response.body
                });
            },
            register: function (username, password) {
                var data = {
                    username: username,
                    password: password
                };
                return $http.post("/auth/register", data).then(function (response) {
                    if (response.data.result == "success") return true;
                    else return response.data.result
                });
            },
            status: function () {
                return $http.get("/auth/status").then(function (response) {
                    return response.data
                });
            }
        }
    }]);
