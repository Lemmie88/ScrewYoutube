$(document).ready(function () {
    document.title = 'Upload Status'

    getVideoStatus()
    setInterval(getVideoStatus, 60000)
})


/**
 * This function sends a request to update video status.
 */
function getVideoStatus() {
    post(window.location.href, videoStatusCallback)
}

/**
 * This function updates the text with the video status.
 * @param data Data from the server
 */
function videoStatusCallback(data) {
    $.each(data, function (url, status) {
        let text;
        switch (status) {
            case 'NEW':
                text = 'Not processed yet'
                break
            case 'PRO':
                text = 'Currently processing'
                break
            case 'UPL':
                text = 'Uploading video to Google Cloud'
                break
            case 'REA':
                text = 'Ready'
                break
        }
        $('.video-list[data-url=' + url + ']').find('.video-status').text(text)
    })
}