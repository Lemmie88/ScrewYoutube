Dropzone.autoDiscover = false

$(document).ready(function () {
    document.title = 'Upload'

    let dropzone = new Dropzone('#upload', {
        paramName: "file",
        maxFilesize: null,
        acceptedFiles: "video/*",
    })

    let statusBtn = $('#status-btn')

    // Prevent user from going to a different page while uploading.
    dropzone.on("addedfile", function () {
        statusBtn.prop('disabled', true)
    })

    // Redirect user to upload status after videos have been uploaded.
    dropzone.on("queuecomplete", function () {
        redirectToUrl(statusBtn.attr('href'))
    })
})
