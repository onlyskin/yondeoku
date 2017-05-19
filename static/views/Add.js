var add_view_model = {
	languages: ['pl', 'ja'],
	new_block_text: '',
	new_block_language: 'pl',
	update_new_block_text: function(text) {
		add_view_model.new_block_text = text;
	},
	update_new_block_language: function(language) {
		add_view_model.new_block_language = language;
	}
};


var Add = {
	view: function() {
		return m('#add',
			m('#add-block-container', [
				m('p', 'Paste your new text into the box below:'),
				m('#controls', [
					m('#input-container',
						m('select', {oninput: m.withAttr('value', add_view_model.update_new_block_language)},
							add_view_model.languages.map(function(l) {
								return m('option', {label: l, value: l}, l)
							}))
					),
					m('#button-container', [
						m('a', {href: "/select",
								oncreate: m.route.link,
								onclick: function(e) {
									ctrl.add_block_request(add_view_model.new_block_text, add_view_model.new_block_language)
								}
								}, 'Add Text'),
						m('a', {href: "/select",
								oncreate: m.route.link}, 'Back to User Page')
					])
				]),
				m('textarea', {id: 'new_block_text',
					oninput: m.withAttr('value', add_view_model.update_new_block_text)})
			])
		);
	}
};
