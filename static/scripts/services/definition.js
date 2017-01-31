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
		}

	};

	return DefinitionService;

});