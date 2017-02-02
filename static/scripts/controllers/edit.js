'use strict';

angular.module('yondeokuApp')
.controller('editCtrl', function($scope, ServerService) {

	$scope.addBlock = (blockText) => {
		ServerService.addBlock(blockText);
	};

});