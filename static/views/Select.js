function UserInfoView(model) {
    return m('#user-info', [
        m('h3', 'Username: ' + model.user.username),
        m('p', {title: 'These are the words that you have marked as definitely known while reading texts.'}, [
            m('#knownWords', model.user.get_known('pl').map((o) => m('', o.word))),
            m('#knownWords', model.user.get_known('ja').map((o) => m('', o.word))),
            ]),
        m('p', {title: 'After this numer of encounters of a given word, it will no longer appear in your vocab lists.'}, 'Threshold: ' + model.user.threshold)
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
                onclick: function(e) {console.log('clicked read');}
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