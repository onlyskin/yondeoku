'use strict';

angular.module('yondeokuApp')
.factory('DataService', function($http) {

	var dataServiceInstance = { userdata: {} };

	dataServiceInstance.getUserdata = function() {
		$http.get('getUserData/flaskTestUser')
		.then(function(response) {
			Object.assign(dataServiceInstance.userdata, response.data);
		});
	};

	return dataServiceInstance;
});