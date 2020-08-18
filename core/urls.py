from django.urls import path

from core.views import index, video

app_name = 'core'

urlpatterns = [
    path('', index, name='index'),
    path('video/<str:url>/', video, name='video'),
]
