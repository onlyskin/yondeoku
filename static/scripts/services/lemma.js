'use strict';

angular.module('yondeokuApp')
.factory('LemmaService', function($http) {

	var LemmaService = {
		getReadLemmas: function (User) {
			var result = {};
			for (var i in User.Blocks) {
				var Block = User.Blocks[i];
				for (var j in Block.lemmaList) {
					var lemmaList = Block.lemmaList[j];
					for (var k in lemmaList) {
						var lemma = lemmaList[k];
						if (!(lemma in result)) {
							result[lemma] = 1;
						} else {
							result[lemma] = result[lemma] + 1;
						}
					}
				}
			}
			return result;
		},
		getNextBlob: function(Block, startIndex) {
			//returns the index of the next token with a fullstop
			var nextBreakpoint = function(start) {
				var tt = Block.tokens.map((t) => t.tokenText);
				for (var i in tt) {
					if (i >= start && tt[i].indexOf('.') >= 0) {
						return parseInt(i);
					}
				}
			};
			return {indexIn: startIndex, indexOut: nextBreakpoint(startIndex)};
		},
		getNextUnreadIndex: function(jBlock, start) {
			if (jBlock.type !== 'jBlock') {
				return [];
			}
			let nextUnreadIndex = jBlock.readSentences.indexOf(false, start);
			return nextUnreadIndex;
		}
	};

	return LemmaService;

});