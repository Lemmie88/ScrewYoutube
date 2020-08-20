import os

from django.shortcuts import render

from core import strings
from core.helpers.helper import get_context
from core.models import Video


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
