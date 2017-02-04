'use strict';

angular.module('yondeokuApp')
.controller('selectCtrl', function($scope) {

	$scope.getReadPercentage = function (Block) {
		let totalTokens = Block.readTokens.length;
		let numberRead = Block.readTokens.filter((i) => { return i == true }).length;
		return Math.round(numberRead / totalTokens * 100);
	};

	$scope.getReadRatio = function (Block) {
		let totalTokens = Block.readTokens.length;
		let numberRead = Block.readTokens.filter((i) => { return i == true }).length;
		return numberRead + '/' + totalTokens;
	};

});
