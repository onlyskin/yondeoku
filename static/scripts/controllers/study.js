'use strict';

angular.module('yondeokuApp')
.controller('studyCtrl', function($scope, $http, ServerService, DataService, LemmaService, $timeout) {

	$scope.ServerService = ServerService;

	var isNew = function (lemma) {
		var knownList = DataService.userdata.known;
		var readDict = LemmaService.getReadLemmas(DataService.userdata);
		var readCount = readDict[lemma]
		if (knownList.indexOf(lemma) >= 0) {
			return false;
		} else if (readCount === undefined) {
			return true;
		} else if (readCount >= DataService.userdata.threshold) {
			return false;
		} else {
			return true;
		}
	};

	var getStudying = function() {
		var currentBlock = $scope.currentBlock;
		var readingPosition = currentBlock.readTokens.indexOf(false);
		var newWords = [];
		while (newWords.length < 10) {
			let blob = LemmaService.getNextBlob(currentBlock, readingPosition);
			let words = currentBlock.bestLemmaList.slice(blob.indexIn, blob.indexOut + 1)
			readingPosition = blob.indexOut + 1;

			let filteredWords = words.filter((w) => isNew(w))
			Array.prototype.push.apply(newWords, filteredWords);
		}
		return newWords;
	};

	$timeout(() => {$scope.newWords = getStudying()}, 150);

});
