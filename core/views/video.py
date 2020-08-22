from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404

from core import strings
from core.forms.video import EditVideoForm
from core.helpers.helper import get_context
from core.models import Video


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

    context = get_context(strings.Page.VIDEO)
    context.update({'video': _video})

    if action == 'success':
        context.update({'toast_title': 'Success', 'toast_message': 'Video has been saved.'})

    return render(request, 'video/video.html', context)


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
