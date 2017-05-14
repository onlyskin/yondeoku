var Add = {
	view: function() {
		return m('#add',
			m('#add-block-container', [
				m('p', 'Paste your new text into the box below:'),
				m('#button-container', [
					m('a', {href: "/select",
							oncreate: m.route.link,
							onclick: function(e) {console.log('add block clicked');}}, 'Add Text'),
					m('a', {href: "/select",
							oncreate: m.route.link}, 'Back to User Page')
				]),
				m('textarea')
			])
		);
	}
};
