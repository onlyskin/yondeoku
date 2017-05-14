var Study = {
	view: function() {
		return m('#study',
			m('#study-container', [
				m('a', {href: "/select", oncreate: m.route.link}, 'Back to user page...'),
				(currentBlock == null ?
					m('Please choose a text to study from your user page...') :
					m('table', {id: 'vocabItems'}, [
						m('thead',
							m('tr', [
								m('th'),
								m('th', 'Word'),
								m('th', 'Guess Meaning')
							])
						),
						m('tbody', newWords.map((w) => {
							return m('tr', {class: 'lemma'}, [
								m('td', {class: 'add no-top',
										onclick: function(e) {console.log('add known lemma')}}, '◎'),
								m('td', {class: 'lemma'}, w.lemma),
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
