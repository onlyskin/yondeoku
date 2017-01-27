'use strict';

angular.module('yondeokuApp')
.service('dataService', function($http) {
 
  this.getUserData = function(callback){
    $http.get('getUserData/flaskTestUser')
    .then(callback)
  };

});