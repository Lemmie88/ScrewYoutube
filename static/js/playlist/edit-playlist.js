$(document).ready(function () {
    document.title = heading.text()

    new Sortable(document.getElementById('list-view'), {
        animation: 150,
        handle: '.material-icons',
    });
})