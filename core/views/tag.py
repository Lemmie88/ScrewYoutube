from django.shortcuts import render

from core import strings
from core.helpers.helper import get_context
from core.models import Tag


def tags(request):
    """
    This function renders the tags page.
    """
    _tags = Tag.objects.all()
    _tags = sorted(_tags, key=lambda t: t.get_number_of_videos(), reverse=True)

    context = get_context(strings.Page.TAGS)
    context.update({'tags': _tags})
    return render(request, 'tag/tags.html', context)
