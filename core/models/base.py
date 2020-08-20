import uuid

from django.db import models
from simple_history.models import HistoricalRecords

from core import strings


class BaseModel(models.Model):
    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    url = models.CharField(
        verbose_name='URL',
        max_length=strings.Constant.DEFAULT_CODE_LENGTH,
        unique=True,
        editable=False
    )

    name = models.CharField(
        verbose_name='Name',
        max_length=250
    )

    description = models.TextField(
        verbose_name='Description',
        null=True,
        blank=True
    )

    visibility = models.CharField(
        max_length=3,
        choices=strings.Constant.VISIBILITY_CHOICES,
        default=strings.Constant.PRIVATE
    )

    date_added = models.DateTimeField(
        verbose_name='Date added',
        auto_now_add=True
    )

    date_modified = models.DateTimeField(
        verbose_name='Date modified',
        auto_now=True
    )

    history = HistoricalRecords(inherit=True)

    class Meta:
        abstract = True
        ordering = ["name"]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(BaseModel, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
