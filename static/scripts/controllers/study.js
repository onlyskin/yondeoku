'use strict';

angular.module('yondeokuApp')
.controller('studyCtrl', function($scope, $http, ServerService, DataService, LemmaService, $timeout) {

	$scope.ServerService = ServerService;

	var isNew = function (lemma) {
		var knownList = DataService.userdata.known;
		var readDict = LemmaService.getReadLemmas(DataService.userdata);
		var readCount = readDict[lemma]
		if (knownList.indexOf(lemma) >= 0) {
			return false;
		} else if (readCount === undefined) {
			return true;
		} else if (readCount >= DataService.userdata.threshold) {
			return false;
		} else {
			return true;
		}
	};

//	$timeout(isNew, 100);

});
