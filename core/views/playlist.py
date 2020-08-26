from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render

from core import strings
from core.forms.playlist import AddPlaylistForm, EditPlaylistForm
from core.helpers.helper import get_context
from core.models import Playlist, Video
from core.helpers.form import Form


def add_playlist(request):
    """
    This function renders the add playlist page.
    """
    videos = Video.objects.all()
    context = get_context(strings.Page.ADD_PLAYLIST)
    context.update({'videos': videos})

    # This is an AJAX call.
    if request.method == 'POST':
        form = AddPlaylistForm(request.POST)

        # Save playlist details.
        if form.is_valid():
            playlist = Playlist.objects.create(
                name=Form.get_title(form.cleaned_data),
                description=Form.get_description(form.cleaned_data))

            # Save videos in playlist.
            videos = request.POST['videos']
            for video in videos.split(','):
                try:
                    video = Video.objects.get(id=video)
                    playlist.add_video(video)
                except Video.DoesNotExist:
                    continue

            return JsonResponse(strings.Constant.SUCCESS)

        else:
            return JsonResponse(dict(form.errors.items()))

    return render(request, 'playlist/add-playlist.html', context)


def add_videos_to_playlist(request):
    """
    This function adds videos to the playlist.
    """
    if request.method == 'POST':
        # Get playlist.
        try:
            _playlist = Playlist.objects.get(url=request.POST['playlist'])
        except Playlist.DoesNotExist:
            return JsonResponse(strings.Constant.SUCCESS)

        original_videos = _playlist.get_videos()
        new_videos = []

        for video_url in request.POST['videos'].split(','):
            try:
                new_videos.append(Video.objects.get(url=video_url))
            except Video.DoesNotExist:
                continue

        # Remove videos from playlist.
        for video in [x for x in original_videos if x not in new_videos]:
            _playlist.delete_video(video)

        # Add videos to playlist.
        for video in [x for x in new_videos if x not in original_videos]:
            _playlist.add_video(video)

    return JsonResponse(strings.Constant.SUCCESS)


def edit_playlist(request, url):
    """
    This function renders the edit playlist page.
    """
    _playlist = get_object_or_404(Playlist, url=url)

    videos = Video.objects.all()
    context = get_context(strings.Page.EDIT_PLAYLIST)
    context.update({'playlist': _playlist, 'videos': videos})

    # This is an AJAX call.
    if request.method == 'POST':
        form = EditPlaylistForm(request.POST)

        if form.is_valid():
            _playlist.delete_all_videos()

            for video_url in request.POST['videos'].split(','):
                try:
                    _playlist.add_video(Video.objects.get(url=video_url))
                except Video.DoesNotExist:
                    continue

            return JsonResponse(strings.Constant.SUCCESS)
        else:
            return JsonResponse(dict(form.errors.items()))

    return render(request, 'playlist/edit-playlist.html', context)
