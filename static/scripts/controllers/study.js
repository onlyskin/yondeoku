'use strict';

angular.module('yondeokuApp')
.controller('studyCtrl', function($scope, $http, ServerService, DataService, LemmaService, DefinitionService, $timeout, $sce) {

	$scope.userdata = DataService.userdata;

	DataService.getUserdata();
	//just for making developing easier atm
	$timeout(() => {$scope.currentBlock = $scope.userdata.Blocks[0]}, 100);

	$scope.ServerService = ServerService;

//	$scope.overviewMode = false;
//	$scope.readingMode = true;

	$scope.setCurrentBlock = function(Block) {
		$scope.currentBlock = Block;
	};

	$scope.renderBlockButton = function(Block) {
		return Block.text.slice(0, 20) + '...';
	};

	$scope.getBlockIndex = function(Block) {
		return $scope.userdata.Blocks.indexOf(Block);
	};

	$scope.startReading = function () {
		$scope.overviewMode = false;
		$scope.readingMode = true;
	};

	$scope.stopReading = function () {
		$scope.overviewMode = true;
		$scope.readingMode = false;
	};

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
		recalculateReadingSection();
	}

	function renderDefinitions (responseJSON) {
		let definitions = responseJSON.data;
		for (var i in definitions) {
			$scope.newWords[i]['definition'] = definitions[i][0];
		}
	};

	//recalculates the variables for the reading section which depend on:
	//1 - which Block is currently being studied
	//2 - any changes to the user's known words
	//3 - any changes to the read sections on any blocks
	function recalculateReadingSection () {
		$scope.currentlyReading = {in: 0, out: 0};
		$scope.currentlyReadingSection = '';
		$scope.newWords = getNewWordsAndSetReadingSection();
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

	$scope.$watchCollection('currentBlock', () => {
		$scope.guessingPhase = true;
		$scope.definitionsPhase = false;
		$scope.readingPhase = false;
		recalculateReadingSection();
	});

	$scope.$watchCollection('userdata', () => {
		recalculateReadingSection();
	});

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

	function getNewWordsAndSetReadingSection() {
		if ($scope.currentBlock === undefined) {
			return [];
		}
		let readingPosition = $scope.currentBlock.readTokens.indexOf(false);
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
	$timeout(() => {$scope.newWords = getNewWordsAndSetReadingSection()}, 150);

});
