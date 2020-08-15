import datetime
import os
import subprocess

import ffmpeg
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from Screw_Youtube.settings import MEDIA_ROOT
from core import strings, scheduler
from core.helpers.helpers import generate_url_code
from core.models import Series, Playlist, Tag
from core.models.base import BaseModel

TO_BE_PROCESSED_DIR = os.path.join(MEDIA_ROOT, 'videos', 'to-be-processed')
PROCESSING_DIR = os.path.join(MEDIA_ROOT, 'videos', 'processing')


def update_filename(instance, filename):
    f"""
    This function changes the filename of the video to <video id>.<extension>.
    :param instance: Instance of the video model
    :param filename: Original filename
    """
    _, file_extension = os.path.splitext(filename)
    filename = str(instance.id) + file_extension
    return os.path.join(TO_BE_PROCESSED_DIR, filename)


class Video(BaseModel):
    link = models.URLField(
        null=True,
        blank=True
    )

    video = models.FileField(
        verbose_name='Video',
        upload_to=update_filename,
        null=True,
        blank=True
    )

    duration = models.DurationField(
        verbose_name='Duration',
        null=True,
        blank=True
    )

    status = models.CharField(
        max_length=3,
        choices=strings.Constants.VIDEO_STATUS_CHOICES,
        default=strings.Constants.NEW
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

    def update_video_duration(self):
        """
        This function updates the duration of the video.
        """
        path = self.video.path
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1',
             path], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        self.duration = datetime.timedelta(seconds=float(result.stdout))
        self.save()

    def convert_to_hls(self):
        """
        This function converts the video to HLS format which makes streaming possible.
        """
        path = self.video.path
        output_dir = os.path.join(PROCESSING_DIR, str(self.id) + '\\')
        filename = os.path.join(output_dir, 'video.m3u8')

        # Make directory to prevent error.
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        try:
            ffmpeg \
                .input(path) \
                .output(filename, format='hls', start_number=0, hls_time=10, hls_list_size=0) \
                .run()

        except FileNotFoundError:
            raise Exception('Download FFMPEG from https://ffmpeg.org/. '
                            'If you have installed it, please restart your console.')

    def generate_thumbnails(self, width=640):
        """
        This function generates thumbnails associated with the video. At 10%, 20%, 30% ... 90% of the video, a
        thumbnail with 640px width is generated. For each thumbnail, a Thumbnail instance is generated.
        """
        from core.models import Thumbnail

        if self.duration is None:
            self.update_video_duration()

        output_dir = os.path.join(PROCESSING_DIR, str(self.id), 'thumbnails')

        # Make directory to prevent error.
        if not os.path.isdir(output_dir):
            os.makedirs(output_dir)

        duration = self.duration.total_seconds()

        index = 1
        for i in range(1, 10):
            # Calculate the duration at 10% of the video etc.
            second = duration * i * 0.1
            filename = os.path.join(output_dir, str(index) + '.png')

            ffmpeg \
                .input(self.video.path, ss=second) \
                .filter('scale', width, -1) \
                .output(filename, vframes=1) \
                .run()

            Thumbnail.objects.create(video=self, position=index, image=filename)

            index += 1

    def delete_thumbnails(self):
        """
        This function deletes all the thumbnails associated with the video.
        """
        from core.models.thumbnail import Thumbnail
        Thumbnail.objects.filter(video=self).delete()

    def is_processing(self):
        """
        This function changes the status of the video to processing.
        """
        self.status = strings.Constants.PROCESSING
        self.save()

    def is_uploading(self):
        """
        This function changes the status of the video to uploading.
        """
        self.status = strings.Constants.UPLOADING
        self.save()

    def is_ready(self):
        """
        This function changes the status of the video to ready.
        """
        self.status = strings.Constants.READY
        self.save()

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Video)


# noinspection PyUnusedLocal
@receiver(post_save, sender=Video)
def process_video(sender, instance, **kwargs):
    scheduler.run()
