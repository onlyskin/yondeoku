'use strict';

angular.module('yondeokuApp')
.directive('devStats', function() {
	return {
		scope: true,
		restrict: 'AE',
		replace: false,
		templateUrl: 'static/templates/devStats.html'
	};
});
