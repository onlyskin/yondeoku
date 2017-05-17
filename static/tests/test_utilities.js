describe('get_percent', function() {

	it('returns 50% for [true, true, false, false]', function() {
		result = get_percent([true, true, false, false]);
		assert.strictEqual(result, '50%');
	});

	it('returns 100% for []', function() {
		result = get_percent([]);
		assert.strictEqual(result, '100%');
	});

	it('returns 100% for [false]', function() {
		result = get_percent([false]);
		assert.strictEqual(result, '0%');
	});

	it('returns 80% for [true, true, true, true, false]', function() {
		result = get_percent([true, true, true, true, false]);
		assert.strictEqual(result, '80%');
	});

	it('returns 0% for [true, true, true]', function() {
		result = get_percent([true, true, true]);
		assert.strictEqual(result, '100%');
	});

});

describe('get_ratio', function() {

	it('returns 2/4 for [true, true, false, false]', function() {
		result = get_ratio([true, true, false, false]);
		assert.strictEqual(result, '2/4');
	});

	it('returns 0/0 for []', function() {
		result = get_ratio([]);
		assert.strictEqual(result, '0/0');
	});

	it('returns 0/1 for [false]', function() {
		result = get_ratio([false]);
		assert.strictEqual(result, '0/1');
	});

	it('returns 4/5 for [true, true, true, true, false]', function() {
		result = get_ratio([true, true, true, true, false]);
		assert.strictEqual(result, '4/5');
	});

	it('returns 3/3 for [true, true, true]', function() {
		result = get_ratio([true, true, true]);
		assert.strictEqual(result, '3/3');
	});

});

