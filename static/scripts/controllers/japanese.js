'use strict';

angular.module('yondeokuApp')
.controller('japaneseCtrl', function($scope, DefinitionService, $timeout) {

	//always a list of objs with a 'lemma' property for the word, and a 'definitions' property
	//[{lemma: '', definitions: [japanese: '', glosses: []]}, ...]
	$scope.newJapaneseWords = [{'lemma': '林檎'}, {'lemma': '猫'}, {'lemma': '犬'}];

	$scope.doneGuessing = () => {
		$scope.$parent.guessingPhase = false;
		$scope.$parent.definitionsPhase = true;
		$scope.newJapaneseWords.forEach((o) => {
			DefinitionService.getJapaneseDefinition(o, (r) => {
				o['definitions'] = r.data;
			});
		});
	};

	$timeout(() => {
		$scope.$parent.setCurrentBlock($scope.$parent.userdata.Blocks[3]);
	}, 100);

});
