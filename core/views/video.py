from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from core import strings
from core.forms.video import EditVideoForm
from core.helpers.helper import get_context
from core.models import Video, Playlist


def videos(request):
    """
    This function renders the videos page.
    """
    _videos = Video.objects.filter(status=strings.Constant.READY)
    context = get_context(strings.Page.VIDEOS)
    context.update({'videos': _videos})
    return render(request, 'video/videos.html', context)


def video(request, url, action=None):
    """
    This function renders the video page.
    """
    _video = get_object_or_404(Video, url=url, status=strings.Constant.READY)
    playlists = Playlist.objects.all()

    context = get_context(strings.Page.VIDEO)
    context.update({'video': _video, 'playlists': playlists})

    if action == 'success':
        context.update({'toast_title': 'Success', 'toast_message': 'Video has been saved.'})

    return render(request, 'video/video.html', context)


def add_video_to_playlists(request):
    """
    This function adds the video to the selected playlists.
    """
    if request.method == 'POST':
        # Get video.
        try:
            _video = Video.objects.get(url=request.POST['video_url'])
        except Video.DoesNotExist:
            return JsonResponse(strings.Constant.SUCCESS)

        original_playlists = _video.get_playlists()
        new_playlists = []

        for playlist in request.POST:
            try:
                new_playlists.append(Playlist.objects.get(name=playlist))
            except Playlist.DoesNotExist:
                continue

        # Remove video from playlists.
        for playlist in [x for x in original_playlists if x not in new_playlists]:
            assert isinstance(playlist, Playlist)
            playlist.delete_video(_video)

        # Add video to playlists.
        for playlist in [x for x in new_playlists if x not in original_playlists]:
            assert isinstance(playlist, Playlist)
            playlist.add_video(_video)

    return JsonResponse(strings.Constant.SUCCESS)


def edit_video(request, url):
    """
    This function renders the edit video page.
    """
    _video = get_object_or_404(Video, url=url)

    context = get_context(strings.Page.EDIT_VIDEO)
    context.update({'video': _video})

    # This is an AJAX call.
    if request.method == 'POST':
        form = EditVideoForm(request.POST)

        # Save video details and redirect to video page.
        if form.is_valid():
            _video.update_details(form.cleaned_data)
            return JsonResponse(strings.Constant.SUCCESS)

        else:
            return JsonResponse(dict(form.errors.items()))

    return render(request, 'video/edit-video.html', context)


def delete_video(request, url):
    """
    This function expects an AJAX call to delete the video.
    """
    _video = get_object_or_404(Video, url=url)
    if request.method == 'POST':
        _video.delete()
    return JsonResponse(strings.Constant.SUCCESS)
