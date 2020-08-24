import uuid

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models.signals import post_delete
from django.dispatch import receiver
from simple_history.models import HistoricalRecords

from core.helpers.helper import generate_url_code
from core.models import Video
from core.models.base import BaseModel


class Playlist(BaseModel):
    name = models.CharField(
        verbose_name='Name',
        max_length=250,
        unique=True
    )

    class Meta:
        ordering = ["name"]
        get_latest_by = ["-date_modified"]

    def get_videos(self):
        """
        This function returns all the videos in a list ordered by position.
        """
        playlist_videos = PlaylistVideo.objects.filter(playlist=self)
        videos = []
        for playlist_video in playlist_videos:
            videos.append(playlist_video.video)
        return videos

    def get_latest_position(self):
        """
        This function gets the last position of the playlist. If there are no videos in playlist, it returns 0.
        """
        playlist_videos = PlaylistVideo.objects.filter(playlist=self)
        if playlist_videos.exists():
            return playlist_videos.last().position

        return 0

    def get_video_position(self, video):
        """
        This function gets the position of the video.
        """
        try:
            return PlaylistVideo.objects.get(playlist=self, video=video).position
        except PlaylistVideo.DoesNotExist:
            return None

    def add_video(self, video):
        """
        This function adds the video to the playlist.
        """
        try:
            PlaylistVideo.objects.create(playlist=self, video=video)
        except ValidationError:
            return

    def add_videos(self, videos):
        """
        This function adds the videos to the playlist.
        """
        for video in videos:
            self.add_video(video)

    def delete_video(self, video):
        """
        This function deletes the video from the playlist.
        """
        try:
            PlaylistVideo.objects.get(playlist=self, video=video).delete()
        except PlaylistVideo.DoesNotExist:
            return

    def delete_videos(self, videos):
        """
        This function deletes the videos from the playlist.
        """
        for video in videos:
            self.delete_video(video)

    def delete_all_videos(self):
        """
        This function deletes all the videos in the playlist.
        """
        PlaylistVideo.objects.filter(playlist=self).delete()

    def have_video(self, video):
        """
        This function checks whether the playlist has a video.
        """
        try:
            PlaylistVideo.objects.get(playlist=self, video=video)
            return True

        except PlaylistVideo.DoesNotExist:
            return False

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Playlist)


class PlaylistVideo(models.Model):
    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    playlist = models.ForeignKey(
        to=Playlist,
        verbose_name='Playlist',
        on_delete=models.CASCADE
    )

    video = models.ForeignKey(
        to=Video,
        verbose_name='Video',
        on_delete=models.CASCADE
    )

    position = models.PositiveSmallIntegerField(
        verbose_name='Position',
        blank=True
    )

    history = HistoricalRecords()

    class Meta:
        verbose_name = 'Playlist Video'
        verbose_name_plural = 'Playlist Video'

        ordering = ["playlist__name", "position"]
        constraints = [
            models.UniqueConstraint(fields=['playlist', 'video'], name='unique_playlist_video'),
            models.UniqueConstraint(fields=['playlist', 'position'], name='unique_playlist_position')
        ]

    def clean(self):
        if self.position is None:
            self.position = self.playlist.get_latest_position() + 1

        print(self.position)
        print(self.video)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(PlaylistVideo, self).save(*args, **kwargs)

    def __str__(self):
        return self.playlist.name + ' - ' + str(self.position)


# noinspection PyUnusedLocal
@receiver(post_delete, sender=PlaylistVideo)
def tidy_position(sender, instance, **kwargs):
    """
    This function tidies the positions of the remaining instances in playlist video.
    For example, if there are 3 videos in a playlist and the first video gets deleted, the other 2 videos will update
    their position to 1 and 2 respectively.
    """
    assert isinstance(instance, PlaylistVideo)

    try:
        playlist = Playlist.objects.get(id=instance.playlist.id)
    except Playlist.DoesNotExist:
        return

    playlist_videos = PlaylistVideo.objects.filter(playlist=playlist)

    position = 1
    for playlist_video in playlist_videos:
        assert isinstance(playlist_video, PlaylistVideo)

        if playlist_video.position != position:
            playlist_video.position = position
            playlist_video.save()

        position += 1
