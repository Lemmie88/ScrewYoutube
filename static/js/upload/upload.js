Dropzone.autoDiscover = false

let dropzone = new Dropzone('#upload', {
    paramName: "file",
    maxFilesize: null,
    acceptedFiles: "video/*",
})

dropzone.on("queuecomplete", function () {
    alert("All files have uploaded ")
})
