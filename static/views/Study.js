var Study = {
	oninit: function(vnode) {
		vnode.state.study_state_manager = study_state_manager;
	},
	view: function(vnode) {
		return m('#study',
			m('#study-container', [
				m('a', {href: "/select", oncreate: m.route.link}, 'Back to user page...'),
				(model.current_block_id == null ?
					m('Please choose a text to study from your user page...') :
					m('table', {id: 'vocabItems'}, [
						m('thead',
							m('tr', [
								m('th'),
								m('th', 'Word'),
								m('th', 'Guess Meaning')
							])
						),
						m('tbody', vnode.state.study_state_manager.new_lemmas.map((l) => {
							return m('tr', {class: 'lemma'}, [
								m('td', {class: 'add no-top',
										onclick: function(e) {console.log('add known lemma')}}, '◎'),
								m('td', {class: 'lemma'}, l.word),
								m('td', {class: 'guess'},
									m('input', {type: 'text'})
								)
							])
						})
						)
					])
				),
				m('a', {href: "/review", oncreate: m.route.link}, 'Done guessing! Show me the definitions.')
			])
		)
	}
}
