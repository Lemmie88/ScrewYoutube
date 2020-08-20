$(document).ready(function () {
    document.title = 'Tags'
})

function clickTag(_url) {
    let url = replaceUrl('tags', 'tag') + _url + '/'
    redirectToUrl(url)
}