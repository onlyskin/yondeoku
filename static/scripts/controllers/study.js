'use strict';

angular.module('yondeokuApp')
.controller('studyCtrl', function($scope, $http, ServerService, DataService, LemmaService, DefinitionService, $timeout, $sce) {

	$scope.guessingPhase = true;
	$scope.definitionsPhase = false;
	$scope.readingPhase = false;

	$scope.doneGuessing = () => {
		$scope.guessingPhase = false;
		$scope.definitionsPhase = true;
		DefinitionService.getDefinitions($scope.newWords, renderDefinitions);
	};

	$scope.doneStudying = () => {
		$scope.definitionsPhase = false;
		$scope.readingPhase = true;
		$scope.currentlyReadingSection = renderCurrentlyReadingSection();
	};

	$scope.doneReading = () => {
		ServerService.setRead($scope.currentBlock.text, $scope.currentlyReading.in, $scope.currentlyReading.out + 1);
		$scope.guessingPhase = true;
		$scope.definitionsPhase = false;
		$scope.readingPhase = false;
		$scope.currentlyReading = {in: 0, out: 0};
		$scope.currentlyReadingSection = '';
		$scope.newWords = getStudying();
	}

	function renderDefinitions (responseJSON) {
		let definitions = responseJSON.data;
		for (var i in definitions) {
			$scope.newWords[i]['definition'] = definitions[i][0];
		}
	};

	$scope.newWords = [];
	$scope.currentlyReading = {in: 0, out: 0};
	$scope.currentlyReadingSection = '';

	function renderPreviousSection () {
		let section = $scope.currentBlock.tokens.slice(0, $scope.currentlyReading.in).map((token) => {
			return token.tokenText;
		}).join(' ');
		return section;		
	};

	function renderCurrentlyReadingSection () {
		let section = $scope.currentBlock.tokens.slice($scope.currentlyReading.in, $scope.currentlyReading.out + 1).map((token) => {
			return token.tokenText;
		}).join(' ');
		return section;
	};

	$scope.$parent.$watch('currentBlock', () => {
		$scope.guessingPhase = true;
		$scope.definitionsPhase = false;
		$scope.readingPhase = false;
		$scope.currentlyReading = {in: 0, out: 0};
		$scope.currentlyReadingSection = '';
		$scope.newWords = getStudying();
	});

/*	$scope.$watch('currentlyReading', () => {
		$scope.currentlyReadingSection = renderCurrentlyReadingSection();
	})
*/

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
		let readingPosition = $scope.currentBlock.readTokens.indexOf(false);
		console.log($scope.currentBlock);
		$scope.currentlyReading['in'] = readingPosition;
		let readingPositionOut = $scope.currentBlock.readTokens.indexOf(false);
		let newWords = [];
		while (newWords.length < 10) {
			let blob = LemmaService.getNextBlob($scope.currentBlock, readingPosition);
			let words = $scope.currentBlock.bestLemmaList.slice(blob.indexIn, blob.indexOut + 1)
			readingPosition = blob.indexOut + 1;
			$scope.currentlyReading['out'] = blob.indexOut;

			let filteredWords = words.filter((w) => isNew(w))
			filteredWords = filteredWords.map((i) => {return {lemma: i}});
			Array.prototype.push.apply(newWords, filteredWords);
		}
		return newWords;
	};

	//just for making developing easier atm
	$timeout(() => {$scope.newWords = getStudying()}, 150);

});
