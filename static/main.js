var model = {
	username: 'Sam',
	user: new User({threshold: 'loading...', username: this.username, known: [], blocks: []}),
	current_block_id: null,
	current_section: null,
	new_words: null
}

var block_info_view_model = {
	expanded: [],
	is_expanded: function(block_id) {
		return this.expanded.indexOf(block_id) != -1;
	},
	expand: function(block_id) {
		if (this.expanded.indexOf(block_id) == -1) {
			this.expanded.push(block_id);
		}
	},
	contract: function(block_id) {
		this.expanded.splice(this.expanded.indexOf(block_id), 1);
	},
	toggle: function(block_id) {
		if (this.is_expanded(block_id)) {
			this.contract(block_id);
		} else {
			this.expand(block_id);
		}
	}
};

var ctrl = {
	initialized: false,
	initialize: function(model) {
		if (!this.initialized) {
			let self = this;
			m.request({
				method: 'GET',
				url: 'getUserData/' + model.username
			})
			.then(function(result) {
				model.user = new User(result);
				self.initialized = true;
			});
		}
	},
}
