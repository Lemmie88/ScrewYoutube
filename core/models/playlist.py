import uuid

from django.db import models
from simple_history.models import HistoricalRecords

import core.strings as strings
from core.helpers.helpers import generate_url_code


class Playlist(models.Model):
    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    url = models.CharField(
        verbose_name='URL',
        max_length=strings.Constants.DEFAULT_CODE_LENGTH,
        unique=True,
        editable=False
    )

    name = models.CharField(
        verbose_name='Name',
        max_length=250
    )

    description = models.TextField(
        verbose_name='Description',
        blank=True,
        null=True
    )

    visibility = models.CharField(
        max_length=3,
        choices=strings.Constants.VISIBILITY_CHOICES,
        default=strings.Constants.PRIVATE,
    )

    date_added = models.DateTimeField(
        verbose_name='Date added',
        auto_now_add=True
    )

    date_modified = models.DateTimeField(
        verbose_name='Date modified',
        auto_now=True
    )

    history = HistoricalRecords()

    class Meta:
        ordering = ["name"]
        get_latest_by = ["-date_modified"]

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Playlist)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Playlist, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
