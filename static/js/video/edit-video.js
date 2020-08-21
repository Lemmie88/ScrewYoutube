$(document).ready(function () {
    document.title = 'Edit: ' + title.val()
})

function clickDelete() {
    modal('Are you sure?', 'This video will be deleted permanently.', 'Delete', deleteVideo)
}

function deleteVideo() {
    let url = replaceUrl('edit', 'delete')
    post(url, redirectToIndex)
}

/**
 * This function submits form data to the API
 */
function submitForm() {
    post(window.location.pathname, submitCallback, editVideoForm.serialize())
}

/**
 * This function displays error if there are errors, otherwise, it will redirect to video page.
 * @param data Data from API
 */
function submitCallback(data) {
    if (isStatusOk(data) === false) {
        displayFormErrors(data)
    } else {
        if (videoStatus === 'REA' && document.referrer.includes('/upload/status/') === false) {
            // Redirect to video page.
            let url = replaceUrl('edit', 'success')
            window.open(url, '_self')
        } else {
            window.open('/upload/status/', '_self')
        }
    }
}