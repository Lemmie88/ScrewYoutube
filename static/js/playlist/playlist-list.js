$(document).ready(function () {
    document.title = 'Playlists'

    resizeCardBlock()
    $(window).on('resize', resizeCardBlock)
})

/**
 * This function resizes the card block so that the text fits besides the thumbnail.
 */
function resizeCardBlock() {
    let padding = 8
    $('.card-block').width($('.playlist-list').width() - $('.card-header').outerWidth() - padding)
}