var model = {
	username: 'Sam',
	user: new User({threshold: 'loading...', username: 'loading...', known: [], blocks: []}),
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
				url: 'user/' + model.username
			})
			.then(function(result) {
				self.set_user_data(model, result);
				self.initialized = true;
			});
		}
	},
	set_user_data: function(model, userdata) {
		model.user = new User(userdata);
	},
	add_block_request: function(text, language) {
		let self = this;
		m.request({
			method: 'POST',
			url: 'add_block/' + model.username,
			data: {text: text, language: language}
		})
		.then(function(result) {
			self.set_user_data(model, result);
		});
	},
	safe_delete_block_request: function(block_id) {
		var confirmation = confirm('Are you sure you want to delete this text?')
		if (confirmation) {
			this._delete_block_request(block_id);
		}
	},
	_delete_block_request: function(block_id) {
		let self = this;
		m.request({
			method: 'POST',
			url: 'delete_block/' + model.username,
			data: {id: block_id}
		})
		.then(function(result) {
			self.set_user_data(model, result);
		});
	}
}






