$(document).ready(function () {
    resizeThumbnail()
    $(window).on('resize', resizeThumbnail)

    resizeCardBlock()
    $(window).on('resize', resizeCardBlock)
})

/**
 * This function resizes the thumbnail according to the screen size.
 */
function resizeThumbnail() {
    let thumbnail = $('.thumbnail')

    if (window.outerWidth <= 576) {
        thumbnail.css('width', '100%')
        thumbnail.css('height', 'auto')
        thumbnail.css('max-height', '300px')
    } else {
        thumbnail.css('width', '')
        thumbnail.css('height', '')
        thumbnail.css('max-height', '')
    }
}

/**
 * This function resizes the card block so that the text fits besides the thumbnail.
 */
function resizeCardBlock() {
    let padding = 8
    if (window.outerWidth <= 576) {
        $('.card-block').width($('.video-list').width() - padding)
    } else {
        $('.card-block').width($('.video-list').width() - $('.card-header').outerWidth() - padding)
    }
}