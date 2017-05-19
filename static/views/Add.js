var add_view_model = {
	new_block_text: '',
	update_new_block_text: function(text) {
		add_view_model.new_block_text = text;
	}
};


var Add = {
	view: function() {
		return m('#add',
			m('#add-block-container', [
				m('p', 'Paste your new text into the box below:'),
				m('#button-container', [
					m('a', {href: "/select",
							oncreate: m.route.link,
							onclick: function(e) {ctrl.add_block_request(add_view_model.new_block_text)}
							}, 'Add Text'),
					m('a', {href: "/select",
							oncreate: m.route.link}, 'Back to User Page')
				]),
				m('textarea', {id: 'new_block_text', oninput: m.withAttr('value', add_view_model.update_new_block_text)})
			])
		);
	}
};
