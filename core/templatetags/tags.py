from django import template

from core.models import *

register = template.Library()


@register.simple_tag
def is_playlist(objects):
    """
    This function checks whether the objects is an instance of playlist.
    """
    # noinspection PyBroadException
    try:
        return isinstance(objects[0], Playlist)
    except Exception:
        return False


@register.simple_tag
def is_video(objects):
    """
    This function checks whether the objects is an instance of playlist.
    """
    # noinspection PyBroadException
    try:
        return isinstance(objects[0], Video)
    except Exception:
        return False


@register.simple_tag
def is_video_in_playlist(_playlist, _video):
    """
    This tag checks whether the playlist has the video.
    """
    assert isinstance(_playlist, Playlist)
    return _playlist.have_video(_video)
