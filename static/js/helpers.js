/**
 * This function updates the navbar by checking the page against the href attribute and add the "active" class.
 * @param page Current page
 */
function updateNavbar(page) {
    $('.nav-link[href="/' + page + '/"]').closest('.nav-item').addClass('active')
}

/**
 * This function updates the heading.
 * @param title
 */
function updateHeading(title=null) {
    if (heading !== null) {
        heading.text(title)
    }
}

/**
 * This function displays a toast.
 * @param title Title of the toast
 * @param message Message of the toast
 * @param duration Duration of the toast (in ms)
 */
function toast(title = 'Message', message = '', duration = 5000) {
    if (message === '') {
        return
    }

    let toast = $('.toast')

    // Set the title and message.
    toast.find('strong').text(title)
    toast.find('.toast-body').text(message)

    // Show and hide toast container accordingly.
    let toastContainer = $('.toast-container')
    toastContainer.show()
    toast.on('hidden.bs.toast', function () {
        toastContainer.hide()
    })

    toast.toast({delay: duration})
    toast.toast('show')
}

/**
 * This function shows the modal.
 * @param title Title of the modal
 * @param body Text message inside the modal
 * @param actionText Text in the action button
 * @param actionFunction This function is activated when action button is clicked
 */
function modal(title, body, actionText, actionFunction) {
    $('#modal-title').text(title)
    $('#modal-body').text(body)

    let modalAction = $('#modal-action')
    modalAction.text(actionText)
    modalAction.off()
    modalAction.click(actionFunction)

    $('#modal').modal('show')
}

/**
 * This function replaces the old string in the url with the new string.
 * @param oldString Original string
 * @param newString New string to replace old string
 * @returns {string} URL
 */
function replaceUrl(oldString, newString) {
    let url = window.location.pathname
    return url.replace(oldString + '/', newString + '/')
}

/**
 * This function reloads the page.
 */
function reloadCallback() {
    location.reload()
}