'use strict';

angular.module('yondeokuApp')
.factory('DataService', function($http) {

	var dataServiceInstance = { userdata: {} };

	dataServiceInstance.getUserdata = function() {
		$http.get('getUserData/Sam')
		.then(function(response) {
			Object.assign(dataServiceInstance.userdata, response.data);
		});
	};

	console.log(dataServiceInstance.userdata);

	return dataServiceInstance;
});