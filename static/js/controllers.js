'use strict';

/* Controllers */

function HomeController($scope, $location, HomeService) {

}
function AuthController($scope, $location, AuthService) {

    $scope.getStatus = function () {
        AuthService.status().then(function (result) {
            $scope.loggedIn = result.status;
            $scope.userId = result.user_id;
        });
    };
    $scope.getStatus();
    $scope.login = function () {
        AuthService.login($scope.username, $scope.password).then(function (result) {
            if (result) {
                $scope.loggedIn = true;
                $scope.loginError = null;
                window.location = "/";
            }
            else {
                $scope.loggedIn = false;
                $scope.loginError = true;
            }
        });
    };

    $scope.register = function () {
        AuthService.register($scope.username, $scope.password).then(function (result) {
            if (result == true) {
                window.location = "/"
            }
            else {
                $scope.registerError = result;
            }
        });
    };
    $scope.logout = function () {
        AuthService.logout().then(function (result) {
            if (result == "success") {
                $scope.loggedIn = false;
                window.location = "/"
            }
            else $scope.loggedIn = true;
        });
    };
}