function KnownWordsView(model, language) {
    var words = model.user.get_known(language);
    return m('.known-display', [
        m('.known-words-title', model.language_map[language] + ' known words: (' + words.length + ')'),
        m('.known-words', words.map((o) => m('', o.word)))
    ])
}

function UserInfoView(model) {
    return m('#user-info', [
        m('h3', 'Username: ' + model.user.username),
        m('', {title: 'These are the words that you have marked as definitely known while reading texts.'},
            model.languages.map(function(l) {return KnownWordsView(model, l);})),
        m('', {title: 'After this numer of encounters of a given word, it will no longer appear in your vocab lists.'}, 'Threshold: ' + model.user.threshold)
    ])
}

function BlockInfoView(model, viewmodel) {
    return m('#block-info', [
        m('', [
            'The current texts you have are: ',
            m('span.note', '(click to expand, read sections marked in red)')
            ]),
        m('a#addBlock', {href: '/add', oncreate: m.route.link}, 'Add a new text.'),
        model.user.blocks.map((b) => m('.block', [
            m('.percent', [m('p', get_percent(b.readSections)), m('p', get_ratio(b.readSections) + ' sections')]),
            m('', {
                    class: (viewmodel.is_expanded(b.id) ? ['expanded block-text'] : 'header-text'),
                    onclick: function(e) {viewmodel.toggle(b.id);}
                }, (viewmodel.is_expanded(b.id) ? b.text : b.text.slice(0, 50) + '...')
            ),
            m('a', {href: "/study",
                oncreate: m.route.link,
                onclick: function(e) {model.current_block_id = b.id;}
                }, 'Read This Text'),
            m('a', {href: "/select",
                oncreate: m.route.link,
                onclick: function(e) {ctrl.safe_delete_block_request(b.id)}}, 'Delete This Text')
        ]))
    ])
}

var Select = {
    view: function() {
        return m("#select", [
            UserInfoView(model),
            BlockInfoView(model, block_info_view_model)
        ]);
    }
}