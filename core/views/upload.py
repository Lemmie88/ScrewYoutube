import os

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render

from core import strings
from core.helpers.helper import get_context
from core.models import Video, Tag


def upload(request):
    """
    This function renders the upload page.
    """
    context = get_context(strings.Page.UPLOAD)

    # Save the uploaded video and start processing.
    if request.method == 'POST':
        file = request.FILES.get('file')
        name, _ = os.path.splitext(str(file))
        Video.objects.create(name=name, video=file)

    return render(request, 'upload/upload.html', context)


def get_videos():
    """
    This function gets all the videos that are not ready and videos that the user has not updated the details.
    """
    tag = Tag.objects.get_or_create(name=strings.Constant.NEW_VIDEO)[0]
    return Video.objects.filter(Q(status=strings.Constant.NEW) |
                                Q(status=strings.Constant.PROCESSING) |
                                Q(status=strings.Constant.UPLOADING) |
                                Q(tag__name=tag))


def upload_status(request):
    """
    This function renders the upload status page.
    """
    context = get_context(strings.Page.UPLOAD_STATUS)
    videos = get_videos()
    context.update({'videos': videos})

    # This returns a dictionary of video url and the status of the video.
    if request.method == 'POST':
        data = {}
        for video in videos:
            data.update({video.url: video.status})
        return JsonResponse(data)

    return render(request, 'upload/upload-status.html', context)
