'use strict';

angular.module('yondeokuApp')
.factory('model', function($http) {

	var modelInstance = { userdata: {known: []} };

	modelInstance.getUserdata = function() {
		$http.get('getUserData/Sam')
		.then(function(response) {
			Object.assign(modelInstance.userdata, response.data);
		});
	};

	modelInstance.currentBlock = undefined;

	return modelInstance;

});

