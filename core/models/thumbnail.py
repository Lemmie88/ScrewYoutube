import uuid

from django.db import models

from core.models import Video


class Thumbnail(models.Model):
    id = models.UUIDField(
        verbose_name='ID',
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    video = models.ForeignKey(
        verbose_name='Video',
        to=Video,
        on_delete=models.CASCADE
    )

    position = models.PositiveSmallIntegerField(
        verbose_name='Position'
    )

    public_url = models.URLField(
        verbose_name='Public URL',
        null=True,
        blank=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['video', 'position'], name='unique_position')
        ]

    def save(self, *args, **kwargs):
        self.full_clean()
        return super(Thumbnail, self).save(*args, **kwargs)

    def __str__(self):
        return self.video.name + ' - ' + str(self.position)
