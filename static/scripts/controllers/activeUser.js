'use strict';

angular.module('yondeokuApp')
.controller('activeUserCtrl', function($scope, dataService, $http, $sce) {

  $scope.overviewMode = false;
  $scope.readingMode = true;

  dataService.getUserData(function(response) { 
      $scope.userdata = response.data;
      $scope.currentBlock = $scope.userdata.Blocks[0]
      console.log($scope.userdata.known['py/set']);
	  });

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

