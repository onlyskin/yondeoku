'use strict';

angular.module('yondeokuApp')
.controller('activeUserCtrl', function($scope, DataService, ServerService, $http, $sce) {

  $scope.userdata = DataService.userdata;

  DataService.getUserdata();

  $scope.ServerService = ServerService;

  $scope.overviewMode = false;
  $scope.readingMode = true;

  $scope.setCurrentBlock = function(Block) {
    $scope.currentBlock = Block;
  };

  $scope.renderBlockButton = function(Block) {
    return Block.text.slice(0, 20) + '...';
  };

  $scope.getBlockIndex = function(Block) {
    return $scope.userdata.Blocks.indexOf(Block);
  };

  $scope.startReading = function () {
    $scope.overviewMode = false;
    $scope.readingMode = true;
  };
 
  $scope.stopReading = function () {
    $scope.overviewMode = true;
    $scope.readingMode = false;
  };

});
