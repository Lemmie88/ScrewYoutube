from django.shortcuts import render, get_object_or_404

from core.helpers.helpers import get_context
from core.models import Video
from core.strings.pages import Pages


def video(request, url):
    """
    This function renders the video page.
    """
    _video = get_object_or_404(Video, url=url)

    context = get_context(Pages.VIDEO)
    context.update({'video': _video})

    return render(request, 'video.html', context)
