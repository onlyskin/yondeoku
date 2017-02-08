'use strict';

angular.module('yondeokuApp')
.directive('jstudy', function() {
	return {
		scope: true,
		restrict: 'AE',
		replace: false,
		templateUrl: 'static/templates/jStudy.html'
	};
});
