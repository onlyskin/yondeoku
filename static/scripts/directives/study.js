'use strict';

angular.module('yondeokuApp')
.directive('study', function() {
	return {
		scope: true,
		restrict: 'AE',
		replace: false,
		templateUrl: 'static/templates/study.html'
	};
});
