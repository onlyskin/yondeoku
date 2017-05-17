// returns string percent of 'true' values in an array
function get_percent(array) {
	if (array.length == 0)
		return '100%';
    var true_values = 0;
    for (var i = 0; i < array.length; i++) {
        if (array[i] === true)
            true_values = true_values + 1;
    }
    return String(Math.round(true_values / array.length * 100)) + '%';
}

//returns string ratio of 'true' values in an array
function get_ratio(array) {
    var true_values = 0;
    for (var i = 0; i < array.length; i++) {
        if (array[i] === true)
            true_values = true_values + 1;
    }
    return true_values + '/' + array.length;
}
