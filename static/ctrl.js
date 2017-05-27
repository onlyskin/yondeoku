'use strict';

angular.module('yondeokuApp')
.controller('mainCtrl', function($scope, model) {

	$scope.addKnownLemma = function(japanese, lemma) {
		ServerService.addKnownLemma(japanese, lemma);
	};

	function renderDefinitions (responseJSON) {
		let definitions = responseJSON.data;
		for (var i in definitions) {
			$scope.newWords[i]['definition'] = definitions[i][0];
		}
	};

	function getDefinitions (definitions, callback) {
		definitions = definitions.map((o) => o.lemma);
		$http.post('getDefs', {words: definitions}, {headers: {'Content-Type': 'application/json'} })
		.then(function (response) {
			callback(response);
		});
	};

});

var ServerService = {

	addKnownLemma: function (japanese, lemma) {
		$http.post('setKnownWords/flaskTestUser', {'japanese': japanese, 'words': [lemma]}, {headers: {'Content-Type': 'application/json'} })
		.then(function (response) {
			Object.assign(model.userdata, response.data);
		});
	},
	deleteKnownLemma: function (japanese, lemma) {
		$http.post('removeKnownWords/flaskTestUser', {'japanese': japanese, 'words': [lemma]}, {headers: {'Content-Type': 'application/json'} })
		.then(function (response) {
			Object.assign(model.userdata, response.data);
		});
	},
	updateThreshold: function (threshold) {
		$http.post('setThreshold/flaskTestUser/' + threshold)
		.then(function (response) {
			Object.assign(model.userdata, response.data);
		});
	},
	setRead: function (blockText, readIn, readOut, japanese) {
		var body = {'blockText': blockText,
					'readIn': readIn,
					'readOut': readOut,
					'readValue': true,
					'japanese': japanese};
		$http.post('setReadTokens/flaskTestUser', body, {headers: {'Content-Type': 'application/json'} })
		.then(function (response) {
			Object.assign(model.userdata, response.data);
		});
	},
	setNotRead: function (blockText, readIn, readOut) {
		var body = {'blockText': blockText,
					'readIn': readIn,
					'readOut': readOut,
					'readValue': false};
		$http.post('setReadTokens/flaskTestUser', body, {headers: {'Content-Type': 'application/json'} })
		.then(function (response) {
			Object.assign(model.userdata, response.data);
		});
	}

};
