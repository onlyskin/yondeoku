'use strict';

angular.module('yondeokuApp')
.controller('selectCtrl', function($scope) {

	//[obj] => [str]
	$scope.filterWordsByLanguage = function (words, language) {
		return words.filter((w) => w.language == language).map((w) => w.word);
	};

	$scope.getReadPercentage = function (Block) {
		let totalSections = Block.sections.length;
		let numberRead = Block.readSections.filter((i) => { return i == true }).length;
		return Math.round(numberRead / totalSections * 100);
	};

	$scope.getReadRatio = function (Block) {
		let totalSections = Block.sections.length;
		let numberRead = Block.readSections.filter((i) => { return i == true }).length;
		return numberRead + '/' + totalSections;
	};

});
