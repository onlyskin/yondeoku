var Select = {
    view: function() {
        return m("#select", [
        	m('#user-info', [
        		m('h3', 'Username: ' + currentUser.username),
        		m('p', {title: 'These are the words that you have marked as definitely known while reading texts.'}, [
        			m('#knownWords', knownPlWords.map((o) => m('', o.word))),
        			m('#knownWords', knownJaWords.map((o) => m('', o.word))),
        			]),
        		m('p', {title: 'After this numer of encounters of a given word, it will no longer appear in your vocab lists.'}, 'Threshold: ' + currentUser.threshold)
        		]),
        	m('#block-info', [
        		m('', [
        			'The current texts you have are: ',
        			m('span.note', '(click to expand, read sections marked in red)')
        			]),
        		m('a#addBlock', {href: '/add', oncreate: m.route.link}, 'Add a new text.'),
        		currentUser.blocks.map((b) => m('.block', [
        			m('p.percent', '% read<br>x/y sentences'),
        			m('', {class: (b.expand ? ['expanded block-text'] : 'header-text')},
        				(b.expand ? b.text : b.text.slice(0, 10) + '...')),
        			m('a', {href: "/study",
					    oncreate: m.route.link,
						onclick: function(e) {console.log('clicked read');}
		    			}, 'Read This Text'),
        			m('a', {href: "/select",
        				oncreate: m.route.link,
        				onclick: function(e) {console.log('clicked delete');}}, 'Delete This Text')
        			])),
        		])
        ])
    }
}