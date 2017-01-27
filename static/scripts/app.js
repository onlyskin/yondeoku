angular.module('yondeokuApp', ['ngSanitize']);

angular.module('yondeokuApp').config(function($interpolateProvider){
    $interpolateProvider.startSymbol('[[').endSymbol(']]');
});
