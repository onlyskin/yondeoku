'use strict';

angular.module('yondeokuApp')
.controller('userCtrl', function($scope, dataService, $http, $sce) {

  $scope.vocabList = [];
  $scope.newBlockText = 'Paste text here.';
  $scope.userSelection = '';
  $scope.vocabListFillerText = {text: 'Select your text on the right and click \'Make List\' above.', show: true};
  $scope.loadingText = 'Downloading new vocab list...';
  $scope.showLoading = false;
  $scope.showTable = false;

  //keeps $scope.userSelection equal to any text the user selects
  //solely within the blockText div, otherwise stays equal to ''
  var selectionChangeListener = function (e) {
    let userSelection = document.getSelection();
    let blockElement = document.getElementById('blockText');
    if (userSelection.anchorNode.parentElement === blockElement &&
                userSelection.focusNode.parentElement === blockElement) {
      $scope.userSelection = userSelection.toString();
    } else {
      $scope.userSelection = '';
    }
  };

  document.addEventListener('selectionchange', selectionChangeListener);
  $scope.$on('$destroy', () => document.removeEventListener('selectionchange', selectionChangeListener));

  dataService.getUserData(function(response) { 
      $scope.userdata = response.data;
      $scope.currentBlock = $scope.userdata.Blocks[0];
	  });
 
  $scope.setReadTokens = function(Block, indexIn, indexOut) {
  	var currentIndex = indexIn;
  	while (currentIndex <= indexOut) {
	  	Block.readTokens[currentIndex] = true;
	  	currentIndex++;
  	}
  	return;
  };

  $scope.renderBlockButton = function(Block) {
    return Block.text.slice(0, 20) + '...';
  };

  $scope.renderDefinition = function(vocabItem) {
    return $sce.trustAsHtml(vocabItem.definition);
  };

  $scope.setCurrentBlock = function(Block) {
    $scope.currentBlock = Block;
  };

  $scope.getVocabList = function(text) {
      $scope.showLoading = true;
      $scope.vocabListFillerText.show = false;
      $http.post('getVocabList/flaskTestUser', {text: text}, {headers: {'Content-Type': 'application/json'} })
      .then(function (response) {
        $scope.showLoading = false;
        $scope.vocabList = response.data.map(obj => {
          return {'lemma': obj['lemma'], 'definition': obj['definition'][0]};
        });
        $scope.showTable = true;
      });
  };

  $scope.addBlock = function(text) {
      $http.post('addBlock/flaskTestUser', {text: text}, {headers: {'Content-Type': 'application/json'} })
      .then(function (response) {
        dataService.getUserData(function(response) { 
            $scope.userdata = response.data;
          });
      });
  };

});

