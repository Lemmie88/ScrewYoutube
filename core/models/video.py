from core import strings
from core.helpers.helpers import generate_url_code
from core.models import Series, Playlist, Tag
from core.models.base import BaseModel
from django.db import models


class Video(BaseModel):
    link = models.URLField(
        null=True,
        blank=True
    )

    video = models.FileField(
        verbose_name='Video',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=3,
        choices=strings.Constants.VIDEO_STATUS_CHOICES,
        default=strings.Constants.UPLOADING
    )

    series = models.ForeignKey(
        to=Series,
        verbose_name='Series',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    playlist = models.ManyToManyField(
        to=Playlist,
        verbose_name='Playlist',
        blank=True
    )

    tag = models.ManyToManyField(
        to=Tag,
        verbose_name='Tag',
        blank=True
    )

    class Meta:
        ordering = ["name"]
        get_latest_by = ["-date_added"]

    def delete_thumbnails(self):
        """
        This function deletes all the thumbnails associated with the video.
        """
        from core.models.thumbnail import Thumbnail
        Thumbnail.objects.filter(video=self).delete()

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Video)
