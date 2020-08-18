from django.shortcuts import render

from core.helpers.helpers import get_context
from core.strings.pages import Pages


def index(request):
    """
    This function renders the videos page.
    """
    context = get_context(Pages.VIDEOS)
    return render(request, 'base.html', context)
