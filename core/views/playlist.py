from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from core import strings
from core.forms.playlist import AddPlaylistForm
from core.helpers.helper import get_context
from core.models import Playlist
from core.helpers.form import Form


def add_playlist(request):
    """
    This function renders the add playlist page.
    """
    context = get_context(strings.Page.ADD_PLAYLIST)

    # This is an AJAX call.
    if request.method == 'POST':
        form = AddPlaylistForm(request.POST)

        # Save playlist details.
        if form.is_valid():
            Playlist.objects.create(
                name=Form.get_title(form.cleaned_data),
                description=Form.get_description(form.cleaned_data))

            return JsonResponse(strings.Constant.SUCCESS)

        else:
            return JsonResponse(dict(form.errors.items()))

    return render(request, 'playlist/add-playlist.html', context)


def edit_playlist(request, url):
    """
    This function renders the edit playlist page.
    """
    _playlist = get_object_or_404(Playlist, url=url)

    context = get_context(strings.Page.EDIT_PLAYLIST)
    context.update({'playlist': _playlist})

    # This is an AJAX call.
    if request.method == 'POST':
        pass
        # form = EditVideoForm(request.POST)
        #
        # # Save video details and redirect to video page.
        # if form.is_valid():
        #     _video.update_details(form.cleaned_data)
        #     return JsonResponse(strings.Constant.SUCCESS)
        #
        # else:
        #     return JsonResponse(dict(form.errors.items()))

    return render(request, 'playlist/edit-playlist.html', context)
