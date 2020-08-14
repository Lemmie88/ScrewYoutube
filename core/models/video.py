from core.helpers.helpers import generate_url_code
from core.models import Series, Playlist, Tag
from core.models.base import BaseModel
from django.db import models


class Video(BaseModel):
    link = models.URLField(
        null=True,
        blank=True
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

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Video)
