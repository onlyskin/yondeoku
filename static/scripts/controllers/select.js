'use strict';

angular.module('yondeokuApp')
.controller('selectCtrl', function($scope) {

	$scope.getReadPercentage = function (Block) {
		if (Block.type === 'jBlock') {
			let totalSentences = Block.readSentences.length;
			let numberRead = Block.readSentences.filter((i) => { return i == true }).length;
			return Math.round(numberRead / totalSentences * 100);
		}
		let totalTokens = Block.readTokens.length;
		let numberRead = Block.readTokens.filter((i) => { return i == true }).length;
		return Math.round(numberRead / totalTokens * 100);
	};

	$scope.getReadRatio = function (Block) {
		if (Block.type === 'jBlock') {
			let totalTokens = Block.sentences.map((o) => o.tokens.length).reduce((a, b) => a + b);
			let numberRead = 0;
			for (var i in Block.readSentences) {
				if (Block.readSentences[i] === true) {
					totalTokens += Block.sentences[i].tokens.length;
				}
			}
			return numberRead + '/' + totalTokens;
		}
		let totalTokens = Block.readTokens.length;
		let numberRead = Block.readTokens.filter((i) => { return i == true }).length;
		return numberRead + '/' + totalTokens;
	};

});
