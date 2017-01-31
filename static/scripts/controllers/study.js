'use strict';

angular.module('yondeokuApp')
.controller('studyCtrl', function($scope, $http, ServerService, DataService, LemmaService, DefinitionService, $timeout, $sce) {

	$scope.guessPhase = true;
	$scope.definitionsPhase = false;

	$scope.doneGuessing = () => {
		$scope.guessPhase = false;
		$scope.definitionsPhase = true;
		DefinitionService.getDefinitions($scope.newWords, renderDefinitions);
	};

	function renderDefinitions (responseJSON) {
		let definitions = responseJSON.data;
		for (var i in definitions) {
			$scope.newWords[i]['definition'] = definitions[i][0];
		}
	};

	$scope.newWords = [];

	$scope.$parent.$watch('currentBlock', () => {
		$scope.newWords = getStudying();
	});

	//watches so that we can update the newWords whenever the known words changes
	$scope.DataServiceKnown = DataService.userdata.known;
	$scope.$watch('DataServiceKnown', () => {$scope.newWords = getStudying();});

	$scope.addKnownLemma = function(lemma) {
		ServerService.addKnownLemma(lemma);
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
		if ($scope.currentBlock === undefined) {
			return [];
		}
		var currentBlock = $scope.currentBlock;
		var readingPosition = currentBlock.readTokens.indexOf(false);
		var newWords = [];
		while (newWords.length < 10) {
			let blob = LemmaService.getNextBlob(currentBlock, readingPosition);
			let words = currentBlock.bestLemmaList.slice(blob.indexIn, blob.indexOut + 1)
			readingPosition = blob.indexOut + 1;

			let filteredWords = words.filter((w) => isNew(w))
			filteredWords = filteredWords.map((i) => {return {lemma: i}});
			Array.prototype.push.apply(newWords, filteredWords);
		}
		return newWords;
	};

	//just for making developing easier atm
	$timeout(() => {$scope.newWords = getStudying()}, 150);

});
