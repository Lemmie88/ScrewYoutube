from django.shortcuts import render, get_object_or_404

from core import strings
from core.helpers.helper import get_context
from core.models import Tag, Video


def tags(request):
    """
    This function renders the tags page.
    """
    _tags = Tag.objects.all()
    _tags = sorted(_tags, key=lambda t: t.get_number_of_videos(), reverse=True)

    context = get_context(strings.Page.TAGS)
    context.update({'tags': _tags})
    return render(request, 'tag/tags.html', context)


def tag(request, url):
    """
    This function renders the tag page.
    """
    _tag = get_object_or_404(Tag, url=url)
    videos = Video.objects.filter(tag=_tag)

    context = get_context(strings.Page.TAG)
    context.update({'tag': _tag, 'videos': videos})

    return render(request, 'tag/tag.html', context)


