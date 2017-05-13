angular.module('yondeokuApp', ['ngSanitize', 'ui.router']);

angular.module('yondeokuApp').config(function($interpolateProvider, $stateProvider, $urlRouterProvider){

    $interpolateProvider.startSymbol('[[').endSymbol(']]');

    $stateProvider
	    .state({name: 'main',
		    	url: '/main',
		    	templateUrl: 'static/templates/main.html',
				controller: 'mainCtrl'
	    })
		.state({name: 'select',
				parent: 'main',
				url: '/select',
				templateUrl: 'static/templates/main-select.html',
				controller: 'mainCtrl'
		})
		.state({name: 'study',
				parent: 'main',
				url: '/study',
				templateUrl: 'static/templates/main-study.html',
				controller: 'mainCtrl'
		})
		.state({name: 'review',
				parent: 'main',
				url: '/review',
				templateUrl: 'static/templates/main-review.html',
				controller: 'mainCtrl'
		})
		.state({name: 'read',
				parent: 'main',
				url: '/read',
				templateUrl: 'static/templates/main-read.html',
				controller: 'mainCtrl'
		})
		.state({name: 'add',
				parent: 'main',
				url: '/add',
				templateUrl: 'static/templates/main-add.html',
				controller: 'mainCtrl'
		});

	$urlRouterProvider.otherwise('main/select');

});
