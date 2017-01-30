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
		}
	};

	return LemmaService;

});