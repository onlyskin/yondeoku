var Read = {
	view: function() {
		return m('#study',
			m('#study-container', [
				m('#reading', currentSection),
				m('a', {href: "/study",
					oncreate: m.route.link,
					onclick: function(e) {
						console.log('Done Reading');
					}}, 'Done reading! Read next section.')
			])
		)
	}
}