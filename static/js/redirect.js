/**
 * This function redirects the user to the index page.
 */
function redirectToIndex() {
    window.open('/',"_self")
}

/**
 * This function redirects user to the selected url.
 * @param url Url to redirect user to
 * @param newTab If true, the user will be redirected to a new tab
 */
function redirectToUrl(url, newTab=false) {
    if (newTab) {
        window.open(url,"_blank")
        return
    }
    window.open(url,"_self")
}

/**
 * This function redirects the user to the videos page.
 */
function redirectToVideos() {
    window.open('/videos/',"_self")
}

/**
 * This function redirects the user to the video page.
 * @param url Video URL
 */
function redirectToVideo(url) {
    window.open('/video/' + url + '/',"_self")
}

/**
 * This function redirects the user to the edit video page.
 * @param url Video URL
 */
function redirectToEditVideo(url) {
    window.open('/video/' + url + '/edit/',"_self")
}

/**
 * This function redirects the user to the playlists page.
 */
function redirectToPlaylists() {
    window.open('/playlists/',"_self")
}

/**
 * This function redirects the user to the playlist page.
 * @param url Playlist URL
 */
function redirectToPlaylist(url) {
    window.open('/playlist/' + url + '/',"_self")
}