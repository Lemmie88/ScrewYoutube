from django.shortcuts import render

from core.helpers.helper import get_context
from core.strings.page import Page


def index(request):
    """
    This function renders the videos page.
    """
    context = get_context(Page.VIDEOS)
    return render(request, 'base.html', context)
