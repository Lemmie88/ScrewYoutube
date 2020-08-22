// Local storage key and value.
const LAYOUT = 'layout'
const GRID_VIEW = 'grid view'
const LIST_VIEW = 'list view'

$(document).ready(function () {
    let layout = getLayout()

    if (layout === GRID_VIEW) {
        showGridView()
    } else {
        showListView()
    }
})

/**
 * This function checks the local storage for the layout view.
 */
function getLayout() {
    let layout = localStorage.getItem(LAYOUT)
    if (layout == null) {
        setGridView()
        return GRID_VIEW
    }

    return layout
}

/**
 * This function saves the layout preference and shows the grid view.
 */
function setGridView() {
    localStorage.setItem(LAYOUT, GRID_VIEW)
    showGridView()
}

/**
 * This function saves the layout preference and shows the list view.
 */
function setListView() {
    localStorage.setItem(LAYOUT, LIST_VIEW)
    showListView()
}

/**
 * This function tweaks the active class and shows the grid view.
 */
function showGridView() {
    $('#toggle-grid-view').addClass('active')
    $('#toggle-list-view').removeClass('active')

    $('#list-view').hide()
    $('#grid-view').show()
}

/**
 * This function tweaks the active class and shows the list view.
 */
function showListView() {
    $('#toggle-list-view').addClass('active')
    $('#toggle-grid-view').removeClass('active')

    $('#grid-view').hide()
    $('#list-view').show()
}