describe('Block', function() {

	it('gets index 2', function() {
		b = {blockdata: {readSections: [true, true, false]}};
		result = Block.prototype.get_next_unread_section_index.apply(b);
		assert.strictEqual(result, 2);
	})

	it('gets index 1', function() {
		b = {blockdata: {readSections: [true, false, true, true, false]}};
		result = Block.prototype.get_next_unread_section_index.apply(b, [0]);
		assert.strictEqual(result, 1);
	})

	it('gets index 4', function() {
		b = {blockdata: {readSections: [true, false, true, true, false]}};
		result = Block.prototype.get_next_unread_section_index.apply(b, [2]);
		assert.strictEqual(result, 4);
	})

	it('gets a, b, c', function() {
		b = new Block({readSections: [true, false], sections: [{lemmas: []}, {lemmas: ['a', 'b', 'c']}]});
		result = b.get_next_unread_section_lemmas();
		assert.deepEqual(result, ['a', 'b', 'c']);
	})


});