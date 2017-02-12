'use strict';

angular.module('yondeokuApp')
.controller('japaneseCtrl', function($scope, DefinitionService, $timeout, LemmaService, ServerService) {

	//always a list of objs with a 'lemma' property for the word, and a 'definitions' property
	//[{lemma: '', definitions: [japanese: '', glosses: []]}, ...]
	$scope.newJapaneseWords = [];

	$scope.jKnown = $scope.$parent.userdata.jKnown;
	$scope.activeSentences = [];

	$scope.doneGuessing = () => {
		$scope.$parent.guessingPhase = false;
		$scope.$parent.definitionsPhase = true;
		$scope.newJapaneseWords.forEach((o) => {
			DefinitionService.getJapaneseDefinition(o, (r) => {
				o['definitions'] = r.data;
			});
		});
	};

	$scope.doneStudying = () => {
		$scope.$parent.definitionsPhase = false;
		$scope.$parent.readingPhase = true;
		$scope.$parent.currentlyReadingSection = renderCurrentlyReadingSection();
	};

	function renderCurrentlyReadingSection () {
		if (JSON.stringify($scope.currentBlock) === "{}") {
			return '';
		}
		let section = $scope.activeSentences.map((s) => s.text).join('');
		return section;
	};

	function relinkJKnown () {
		$scope.jKnown = $scope.$parent.userdata.jKnown;
	};

	function isNew (token) {
		return $scope.jKnown.indexOf(token) === -1;
	};

	function recalculateActiveSentencesAndNewWords () {
		let maxLength = 8;
		$scope.activeSentences = [];
		let start = 0;
		let newWords = [];
		let done = false;
		while (!done) {
			let nextUnreadIndex = LemmaService.getNextUnreadIndex($scope.$parent.currentBlock, start);
			start = nextUnreadIndex + 1;
			let nextUnreadSentence = $scope.$parent.currentBlock.sentences[nextUnreadIndex];
			let tokens = nextUnreadSentence.tokens;
			let newTokens = tokens.filter((t) => isNew(t));

			if (newWords.length + newTokens.length <= maxLength || newWords.length === 0) {
				Array.prototype.push.apply(newWords, newTokens);
				$scope.activeSentences.push(nextUnreadSentence);
			} else {
				done = true;
			}

		}
		//potentially problematic as reassigns newJapaneseWords? If we set any watches will fail
		$scope.newJapaneseWords = [];
		newWords = newWords.map((w) => {
			return {'lemma': w};
		});
		Array.prototype.push.apply($scope.newJapaneseWords, newWords);
		let inValue = $scope.$parent.currentBlock.sentences.indexOf($scope.activeSentences[0]);
		let outValue = $scope.$parent.currentBlock.sentences.indexOf($scope.activeSentences.slice(-1)[0]);
		console.log('in', inValue);
		console.log('out', outValue);
		$scope.$parent.currentlyReading.in = inValue;
		$scope.$parent.currentlyReading.out = outValue;
		console.log('updated to', $scope.$parent.currentlyReading);
		console.log('recalculate active sentences complete');
	};

	$scope.$parent.$watchCollection('curentBlock', () => {
		console.log('currentBlock parent watch triggered $scope.activeSentences to be recalculated');
		recalculateActiveSentencesAndNewWords();
	});

	$scope.$parent.$watchCollection('userdata', () => {
		relinkJKnown();
		recalculateActiveSentencesAndNewWords();
	})

});
