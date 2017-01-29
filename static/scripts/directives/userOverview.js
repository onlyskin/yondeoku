'use strict';

angular.module('yondeokuApp')
.directive('userOverview', function() {
	return {
		scope: true,
		restrict: 'AE',
		replace: false,
		templateUrl: 'static/templates/userOverview.html'
	};
});
