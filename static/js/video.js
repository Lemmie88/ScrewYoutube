let video = $('#video')
let title = $('#title')
let description = $('#description')


$(document).ready(function () {
    document.title = title.text()
    videojs('video')

    calculateVideoHeight()
    $(window).resize(calculateVideoHeight)
})

function calculateVideoHeight() {
    /**
     * This function calculate the height of the video based on the ratio 16:9.
     */
    video.height(video.width() / 16 * 9)
    video.closest('div').height(video.height())
}