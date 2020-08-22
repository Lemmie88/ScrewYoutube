$(document).ready(function () {

})

function submitForm(page) {
    let form = $('#playlist-form')

    if (page.toString().includes('add')) {
        post(window.location.pathname, addPlaylistCallback, form.serialize())
    }
}

/**
 * This function displays error if there are errors, otherwise, it will redirect to playlists page.
 * @param data Data from API
 */
function addPlaylistCallback(data) {
    if (isStatusOk(data) === false) {
        displayFormErrors(data)
    } else {
        // TODO: Redirect to playlists page.
    }
}