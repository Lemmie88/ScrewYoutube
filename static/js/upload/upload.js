Dropzone.autoDiscover = false

$(document).ready(function () {
    document.title = 'Upload'

    let dropzone = new Dropzone('#upload', {
        paramName: "file",
        maxFilesize: null,
        acceptedFiles: "video/*",
    })

    dropzone.on("queuecomplete", function () {
        alert("All files have uploaded ")
    })
})
