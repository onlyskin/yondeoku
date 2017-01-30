'use strict';

angular.module('yondeokuApp')
.factory('LemmaService', function($http) {

	var LemmaService = {
		getReadLemmas: function(Blocks) {
			var result = {};
			var inspect = {};
			for (var i in Blocks) {
				var Block = Blocks[i];
				for (var j in Block.lemmaList) {
					var lemmaList = Block.lemmaList[j];
					console.log(lemmaList);
					console.log(typeof(lemmaList));
					var token = Block.tokens[j].tokenText;
					for (var k in lemmaList) {
						var lemma = lemmaList[k];
						if (!(lemma in result)) {
							result[lemma] = 1;
							inspect[lemma] = [token];
						} else {
							result[lemma] = result[lemma] + 1;
							inspect[lemma].push(token);
						}
					}
				}
			}
			return result;
//			return inspect;
		}
	};

	return LemmaService;

});