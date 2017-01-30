'use strict';

angular.module('yondeokuApp')
.factory('ServerService', function($http, DataService) {

	var ServerService = {

		addKnownLemma: function (lemma) {
			$http.post('setKnownWords/flaskTestUser', [lemma], {headers: {'Content-Type': 'application/json'} })
			.then(function (response) {
				Object.assign(DataService.userdata, response.data);
			});
		},
		deleteKnownLemma: function (lemma) {
			$http.post('removeKnownWords/flaskTestUser', [lemma], {headers: {'Content-Type': 'application/json'} })
			.then(function (response) {
				Object.assign(DataService.userdata, response.data);
			});
		},
		addBlock: function (blockText) {
			var body = {'text': blockText};
			$http.post('addBlock/flaskTestUser', body, {headers: {'Content-Type': 'application/json'} })
			.then(function (response) {
				Object.assign(DataService.userdata, response.data);
			});
		},
		deleteBlock: function (blockText) {
			var body = {'text': blockText};
			$http.post('deleteBlock/flaskTestUser', body, {headers: {'Content-Type': 'application/json'} })
			.then(function (response) {
				Object.assign(DataService.userdata, response.data);
			});
		},
		updateThreshold: function (threshold) {
			$http.post('setThreshold/flaskTestUser/' + threshold)
			.then(function (response) {
				Object.assign(DataService.userdata, response.data);
			});
		},
		setRead: function (blockText, readIn, readOut) {
			var body = {'blockText': blockText,
						'readIn': readIn,
						'readOut': readOut,
						'readValue': true};
			$http.post('setReadTokens/flaskTestUser', body, {headers: {'Content-Type': 'application/json'} })
			.then(function (response) {
				Object.assign(DataService.userdata, response.data);
			});
		},
		setNotRead: function (blockText, readIn, readOut) {
			var body = {'blockText': blockText,
						'readIn': readIn,
						'readOut': readOut,
						'readValue': false};
			$http.post('setReadTokens/flaskTestUser', body, {headers: {'Content-Type': 'application/json'} })
			.then(function (response) {
				Object.assign(DataService.userdata, response.data);
			});
		}

	};

	return ServerService;

});