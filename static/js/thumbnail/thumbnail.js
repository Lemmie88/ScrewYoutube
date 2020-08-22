let thumbnail
let intervalId

$(document).ready(function () {
    let thumbnail = $('.thumbnail')
    thumbnail.hover(onThumbnailHover, offThumbnailHover)
})

/**
 * This function breaks down the url into various groups.
 * @param src URL source
 */
function regexThumbnail(src) {
    let regex = /(^.*thumbnails\/)(.*)(\.png)/
    let groups = src.toString().match(regex)

    let url = groups[1]
    let position = parseInt(groups[2])
    let extension = groups[3]

    return [url, position, extension]
}

/**
 * This function changes the thumbnail between position 1 to 9.
 * @param overridePosition If this is not null, the thumbnail position is overrode.
 */
function changeThumbnail(overridePosition = null) {
    let src = thumbnail.attr('src')
    let [url, position, extension] = regexThumbnail(src)

    if (++position > 9) {
        position = 1
    }

    if (overridePosition != null) {
        position = overridePosition
    }

    thumbnail.attr('src', url + position.toString() + extension)
}

/**
 * This function starts a loop which changes the thumbnail every second.
 */
function onThumbnailHover() {
    thumbnail = $(this)
    changeThumbnail()
    intervalId = setInterval(changeThumbnail, 1000)
}

/**
 * This function stops the loop and resets the thumbnail to the first position.
 */
function offThumbnailHover() {
    clearInterval(intervalId)
    changeThumbnail(1)
}