'use strict';

angular.module('yondeokuApp')
.controller('studyCtrl', function($scope, $http, ServerService, DataService, LemmaService, DefinitionService, $timeout, $sce) {

	let readDict = LemmaService.getReadLemmas(DataService.userdata);

	$scope.currentBlock = null;
	$scope.userdata = DataService.userdata;

	DataService.getUserdata();

	$scope.ServerService = ServerService;
	$scope.safeDeleteBlock = function(blockText) {
		let r = confirm("Are you sure you want to delete this text?");
		if (r === true) {
			ServerService.deleteBlock(blockText);
		}
	};

	$scope.setCurrentBlock = function(Block) {
		$scope.currentBlock = Block;
	};

	$scope.renderBlockButton = function(Block) {
		return Block.text.slice(0, 20) + '...';
	};

	$scope.getBlockIndex = function(Block) {
		return $scope.userdata.Blocks.indexOf(Block);
	};

	function getBlockIndexFromText (blockText) {
		let blockTextMap = $scope.userdata.Blocks.map((i) => i.text);
		return blockTextMap.indexOf(blockText);
	}

	function relinkCurrentBlock() {
		let i = getBlockIndexFromText($scope.currentBlock.text);
		$scope.currentBlock = $scope.userdata.Blocks[i];
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
		let firstRepeat = $$childHead;
		console.log($$childHead);
	};

	$scope.doneReading = () => {
		ServerService.setRead($scope.currentBlock.text, $scope.currentlyReading.in, $scope.currentlyReading.out + 1);
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
	$scope.previousSection = '';
	$scope.nextSection = '';

	function setPreviousSection () {
		if ($scope.currentBlock === null) {
			return '';
		}
		let section = $scope.currentBlock.tokens.slice($scope.currentlyReading.in - 100, $scope.currentlyReading.in).map((token) => {
			return token.tokenText;
		}).join(' ');
		return section;
	};

	function setNextSection () {
		if ($scope.currentBlock === null) {
			return '';
		}
		let section = $scope.currentBlock.tokens.slice($scope.currentlyReading.out + 1, $scope.currentlyReading.out + 51).map((token) => {
			return token.tokenText;
		}).join(' ');
		return section;
	};

	function renderCurrentlyReadingSection () {
		if ($scope.currentBlock === null) {
			return '';
		}
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
		readDict = LemmaService.getReadLemmas(DataService.userdata);
		relinkCurrentBlock();
		recalculateReadingSection();
	});

	$scope.addKnownLemma = function(lemma) {
		ServerService.addKnownLemma(lemma);
	};

	function isNew (lemma) {
		var knownList = DataService.userdata.known;
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
		if ($scope.currentBlock === null) {
			return [];
		}
		let readingPosition = $scope.currentBlock.readTokens.indexOf(false);
		$scope.currentlyReading['in'] = readingPosition;
		$scope.previousSection = setPreviousSection();
		let readingPositionOut = $scope.currentBlock.readTokens.indexOf(false);
		let newWords = [];
		while (newWords.length < 10) {
			let blob = LemmaService.getNextBlob($scope.currentBlock, readingPosition);
			let words = $scope.currentBlock.bestLemmaList.slice(blob.indexIn, blob.indexOut + 1)

			let filteredWords = words.filter((w) => isNew(w))
			filteredWords = filteredWords.map((i) => {return {lemma: i}});

			//if there is something in newWords already, then we'll make sure the next
			//sentence doesn't make it go over 10 and if it does just return the current
			//newWords instead of adding this one
			if (newWords.length !== 0) {
				if (newWords.length + filteredWords.length > 10) {
					$scope.nextSection = setNextSection();
					return newWords;
				}
			}

			//otherwise we need to add it even if it makes it exceed 10
			readingPosition = blob.indexOut + 1;
			$scope.currentlyReading['out'] = blob.indexOut;
			Array.prototype.push.apply(newWords, filteredWords);
		}
		$scope.nextSection = setNextSection();
		return newWords;
	};

});
