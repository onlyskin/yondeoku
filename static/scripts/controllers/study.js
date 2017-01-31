'use strict';

angular.module('yondeokuApp')
.controller('studyCtrl', function($scope, $http, ServerService, DataService, LemmaService, $timeout) {

	$scope.guessPhase = true;
	$scope.definitionsPhase = false;

	$scope.newWords = [];

	$scope.$parent.$watch('currentBlock', () => {
		$scope.newWords = getStudying();
	});

	$scope.addKnownLemma = function(lemma) {
		ServerService.addKnownLemma(lemma);
		$scope.newWords = getStudying();
	};

	function isNew (lemma) {
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

	function getStudying() {
		console.log('executed');
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

	//just for making developing easier atm
	$timeout(() => {$scope.newWords = getStudying()}, 150);

});
