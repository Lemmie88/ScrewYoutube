from django.shortcuts import redirect


# noinspection PyUnusedLocal
def index(request):
    return redirect('/videos')
