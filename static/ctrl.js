'use strict';

angular.module('yondeokuApp')
.controller('mainCtrl', function($scope, model) {

	$scope.renderCurrentSections = function() {
		return 'this is an example of a rendered section'
	}

	model.getUserdata();
	$scope.model = model;

	$scope.addBlock = (blockText) => {
		ServerService.addBlock(blockText);
	};

	$scope.setCurrentBlock = function(Block) {
		model.currentBlock = Block;
	};

	//[obj] => [str]
	$scope.filterWordsByLanguage = function (words, language) {
		return words.filter((w) => w.language == language).map((w) => w.word);
	};

	$scope.getReadPercentage = function (Block) {
		let totalSections = Block.sections.length;
		let numberRead = Block.readSections.filter((i) => { return i == true }).length;
		return Math.round(numberRead / totalSections * 100);
	};

	$scope.getReadRatio = function (Block) {
		let totalSections = Block.sections.length;
		let numberRead = Block.readSections.filter((i) => { return i == true }).length;
		return numberRead + '/' + totalSections;
	};

	$scope.safeDeleteBlock = function(blockText) {
		let r = confirm("Are you sure you want to delete this text?");
		if (r === true) {
			ServerService.deleteBlock(blockText);
		}
	};

	$scope.renderBlockButton = function(Block) {
		return Block.text.slice(0, 20) + '...';
	};

	$scope.getBlockIndex = function(Block) {
		return $scope.model.userdata.blocks.indexOf(Block);
	};

	function getBlockIndexFromText (blockText) {
		let blockTextMap = $scope.model.userdata.blocks.map((i) => i.text);
		return blockTextMap.indexOf(blockText);
	}

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
	addBlock: function (blockText) {
		var body = {'text': blockText};
		$http.post('addBlock/flaskTestUser', body, {headers: {'Content-Type': 'application/json'} })
		.then(function (response) {
			Object.assign(model.userdata, response.data);
		});
	},
	deleteBlock: function (blockText) {
		var body = {'text': blockText};
		$http.post('deleteBlock/flaskTestUser', body, {headers: {'Content-Type': 'application/json'} })
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
