$(document).ready(function () {
    document.title = title.text()
    videojs('video')

    calculateVideoHeight()
    $(window).resize(calculateVideoHeight)
})

/**
 * This function calculate the height of the video based on the ratio 16:9.
 */
function calculateVideoHeight() {
    video.height(video.width() / 16 * 9)
    video.closest('div').height(video.height())
}

/**
 * This function sends the playlist data to the API.
 */
function addVideoToPlaylist() {
    let data = $('#playlist-modal').find('form').serialize()
    post('/video/add-playlist/', reloadCallback, data)
}