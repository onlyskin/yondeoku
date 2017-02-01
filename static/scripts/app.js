angular.module('yondeokuApp', ['ngSanitize', 'ui.router']);

angular.module('yondeokuApp').config(function($interpolateProvider, $stateProvider, $urlRouterProvider){

    $interpolateProvider.startSymbol('[[').endSymbol(']]');

    $stateProvider
	    .state({name: 'main',
		    	url: '/main',
		    	templateUrl: 'static/templates/main.html',
		    	controller: 'studyCtrl'
	    })
		.state({name: 'select',
				parent: 'main',
				url: '/select',
				templateUrl: 'static/templates/main-select.html',
		})
		.state({name: 'study',
				parent: 'main',
				url: '/study',
				templateUrl: 'static/templates/main-study.html',
		});

	$urlRouterProvider.otherwise('main/select');

});
