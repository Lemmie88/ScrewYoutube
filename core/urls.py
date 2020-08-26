from django.urls import path

from core.views import *

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),

    path('videos/', videos, name='videos'),
    path('video/add-playlist/', add_video_to_playlists, name='add_video_to_playlists'),
    path('video/<str:url>/', video, name='video'),
    path('video/<str:url>/edit/', edit_video, name='edit_video'),
    path('video/<str:url>/delete/', delete_video, name='delete_video'),
    path('video/<str:url>/<str:action>/', video, name='video'),

    path('tags/', tags, name='tags'),
    path('tag/<str:url>/', tag, name='tag'),

    path('playlists/', playlists, name='playlists'),
    path('playlists/add/', add_playlist, name='add_playlist'),
    path('playlists/add-video/', add_videos_to_playlist, name='add_videos_to_playlist'),
    path('playlist/<str:url>/', playlist, name='playlist'),
    path('playlist/<str:url>/edit/', edit_playlist, name='edit_playlist'),
    path('playlist/<str:url>/delete/', delete_playlist, name='delete_playlist'),

    path('upload/', upload, name='upload'),
    path('upload/status/', upload_status, name='upload_status'),
]
