from django.urls import path

from core.views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),

    path('videos/', videos, name='videos'),
    path('video/<str:url>/', video, name='video'),
    path('video/<str:url>/edit/', edit_video, name='edit_video'),
    path('video/<str:url>/delete/', delete_video, name='delete_video'),
    path('video/<str:url>/<str:action>/', video, name='video'),

    path('tags/', tags, name='tags'),
]
