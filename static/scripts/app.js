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
				controller: 'selectCtrl'
		})
		.state({name: 'study',
				parent: 'main',
				url: '/study',
				templateUrl: 'static/templates/main-study.html'
		})
		.state({name: 'add',
				parent: 'main',
				url: '/add',
				templateUrl: 'static/templates/main-add.html',
				controller: 'editCtrl'
		});

	$urlRouterProvider.otherwise('main/select');

});
