/**
 * This function redirects the user to the index page.
 */
function redirectToIndex() {
    window.open('/',"_self")
}

/**
 * This function redirects user to the selected url.
 * @param url Url to redirect user to
 * @param newTab If true, the user will be redirected to a new tab
 */
function redirectToUrl(url, newTab=false) {
    if (newTab) {
        window.open(url,"_blank")
        return
    }
    window.open(url,"_self")
}

/**
 * This function redirects the user to the video page.
 * @param url Video URL
 */
function redirectToVideo(url) {
    window.open('/video/' + url + '/',"_self")
}

/**
 * This function redirects the user to the edit video page.
 * @param url Video URL
 */
function redirectToEditVideo(url) {
    window.open('/video/' + url + '/edit/',"_self")
}


/**
 * This function updates the navbar by checking the page against the href attribute and add the "active" class.
 * @param page Current page
 */
function updateNavbar(page) {
    $('.nav-link[href="/' + page + '/"]').closest('.nav-item').addClass('active')
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

    // Set the height of the toast wrapper.
    // $('.toast-wrapper').height(window.outerHeight - $('nav').outerHeight())

    // Set the title and message.
    toast.find('strong').text(title)
    toast.find('.toast-body').text(message)

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