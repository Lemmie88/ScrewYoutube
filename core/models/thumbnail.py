from django.db import models

from core.models import Video


class Thumbnail(models.Model):
    video = models.ForeignKey(
        verbose_name='Video',
        to=Video,
        on_delete=models.CASCADE
    )

    position = models.PositiveSmallIntegerField(
        verbose_name='Position'
    )

    image = models.FileField(
        verbose_name='Image',
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
