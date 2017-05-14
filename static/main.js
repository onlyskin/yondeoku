var root = document.querySelector('#wrapper');

m.route(root, "/select", {
    "/select": Select,
    "/add": Add,
    "/study": Study,
    "/review": Review,
    "/read": Read
})

