'use strict';

angular.module('yondeokuApp')
.factory('DefinitionService', function($http) {

	var DefinitionService = {

		getDefinitions: function (definitions, callback) {
			definitions = definitions.map((o) => o.lemma);
			$http.post('getDefs', {words: definitions}, {headers: {'Content-Type': 'application/json'} })
			.then(function (response) {
				callback(response);
			});
		},

		//gets a single definition object from a single word
		//the response contains [{japanese: '', glosses: []}, ...]
		getJapaneseDefinition: function(definition, callback) {
			let lemma = definition.lemma;
			$http.post('getJapaneseDef', {word: lemma}, {headers: {'Content-Type': 'application/json'} })
			.then(function (r) {
				callback(r);
			});
		}

	};

	return DefinitionService;

});