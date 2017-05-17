describe('block_info_view_model', function() {

	it('calling expand with block_id 3 returns is_expanded for 3', function() {
		block_info_view_model.expand(3);
		assert.isTrue(block_info_view_model.is_expanded(3));
	});

	it('adding 3 then removing 3 returns false for 3', function() {
		block_info_view_model.expand(3);
		block_info_view_model.contract(3);
		assert.isFalse(block_info_view_model.is_expanded(3));
	});

});

