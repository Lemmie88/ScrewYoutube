/**
 * This function checks to see whether the API returns {'status': 'ok'}.
 * @param data Data from the API
 */
function isStatusOk(data) {
    for (let key in data) {
        if (data.hasOwnProperty(key)) {
            if (key === 'status' && data[key] === 'ok') {
                return true
            }
        }
    }
    return false
}

/**
 * This function displays an error on an element.
 * @param element jQuery instance
 * @param error Error message as string
 */
function displayError(element, error) {
    element.addClass('is-invalid')
    element.after('<div class="invalid-feedback">' + error + '</div>')
}

/**
 * This function displays all the error messages.
 * @param data Data from the API
 */
function displayFormErrors(data) {
    removeFormErrors()

    for (let name in data) {
        let element = $('[name ="' + name + '"]')

        if (data.hasOwnProperty(name)) {
            for (let i = 0; i < data[name].length; i++) {
                displayError(element, data[name][i])
            }
        }
    }
}

/**
 * This function removes errors on an element.
 * @param element jQuery instance
 */
function removeError(element) {
    element.removeClass('is-invalid')
    element.closest('div').find('.invalid-class').remove()
}

/**
 * This function removes errors in a form.
 */
function removeFormErrors() {
    let elements = $('form').find('.form-control')
    for (let i = 0; i < elements.length; i++) {
        removeError($(elements[i]))
    }
}

/**
 * This function makes an AJAX call to the URL.
 */
function post(url, callback, postData = null) {
    try {
        // noinspection JSUnusedGlobalSymbols
        $.ajax({
            url: url,
            type: 'POST',
            headers: {
                'X-CSRFToken': get_csrf_token()
            },
            data: postData,
            success: function (data) {
                callback(data)
            },
            error: function (data) {
                console.error(data)
            }
        })
    } catch (error) {
        console.error(error)
    }
}

/**
 * This function retrieves the CSRF token.
 */
function get_csrf_token() {
    if (DEBUG === 'True') {
        return Cookies.get('csrftoken')
    } else {
        return document.querySelector('[name=csrfmiddlewaretoken]').value
    }
}