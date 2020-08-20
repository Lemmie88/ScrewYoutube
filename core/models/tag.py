from django.db import models

from core.helpers.helper import *
from core.models.base import BaseModel


class Tag(BaseModel):
    image = models.ImageField(
        verbose_name='Image',
        null=True,
        blank=True
    )

    colour = models.CharField(
        verbose_name='Colour',
        max_length=7,
        blank=True
    )

    class Meta:
        ordering = ["name"]

    def get_number_of_videos(self):
        from .video import Video
        videos = Video.objects.filter(tag=self)
        return len(videos)

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Tag)

        # Generate colour for tag.
        if self.colour is '' or self.colour is None:
            self.colour = random_colour()
