from django import template

from core.models import Playlist

register = template.Library()


@register.simple_tag
def is_playlist(objects):
    """
    This function checks whether the objects is an instance of playlist.
    """
    return isinstance(objects[0], Playlist)


@register.simple_tag
def is_video_in_playlist(playlist, video):
    """
    This tag checks whether the playlist has the video.
    """
    assert isinstance(playlist, Playlist)
    return playlist.have_video(video)
