import datetime
import os
import shutil
import subprocess

# noinspection PyPackageRequirements
import ffmpeg
from django.core.files.storage import FileSystemStorage
from django.db import models
from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from ScrewYoutube import settings
from core import strings, scheduler
from core.helpers.helper import generate_url_code
from core.helpers.storage import upload_file, delete_folder
from core.helpers.form import Form
from core.models import BaseModel, Series, Playlist, Tag

VIDEO_DIR = os.path.join(settings.TEMP_ROOT, 'videos')
ORIGINAL_DIR = os.path.join(VIDEO_DIR, 'original')
PROCESSING_DIR = os.path.join(VIDEO_DIR, 'processing')


def update_filename(instance, filename):
    """
    This function changes the filename of the video to <video id>.<extension>.
    :param instance: Instance of the video model
    :param filename: Original filename
    """
    _, file_extension = os.path.splitext(filename)
    return str(instance.id) + file_extension


class Video(BaseModel):
    video = models.FileField(
        verbose_name='Video',
        upload_to=update_filename,
        storage=FileSystemStorage(location=ORIGINAL_DIR),
        null=True,
        blank=True
    )

    public_url = models.URLField(
        verbose_name='Public URL',
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
        choices=strings.Constant.VIDEO_STATUS_CHOICES,
        default=strings.Constant.NEW
    )

    link = models.URLField(
        verbose_name='Link',
        help_text='For example, this can be the IMDB page URL of the video.',
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

    def update_details(self, cleaned_data):
        """
        This function updates the video details from the form and removes the new video tag.
        """
        self.name = Form.get_title(cleaned_data)
        self.description = Form.get_description(cleaned_data)
        self.save()

        self.remove_new_video_tag()

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

    def update_public_url(self, url):
        """
        This function updates the public url of video.
        """
        self.public_url = url
        self.save()

    def convert_to_hls(self):
        """
        This function converts the video to HLS format which makes streaming possible.
        """
        path = self.video.path
        output_dir = self.get_processing_dir()
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
        thumbnail with 640px width is generated.
        """
        self.delete_thumbnails()

        if self.duration is None:
            self.update_video_duration()

        output_dir = self.get_processing_dir(thumbnails=True)

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

            index += 1

    def upload_hls_video(self):
        """
        This function uploads the video in HLS format to Google Cloud.
        """
        remote_location = self.get_remote_storage_dir()
        for filename in os.listdir(self.get_processing_dir()):
            if filename.endswith('.m3u8') or filename.endswith('.ts'):
                file_path = os.path.join(self.get_processing_dir(), filename)
                public_url = upload_file(filename, file_path, remote_location)

                if filename.endswith('.m3u8'):
                    self.update_public_url(public_url)

    def upload_thumbnails(self):
        """
        This function uploads the thumbnails to Google Cloud.
        """
        from core.models import Thumbnail

        remote_location = self.get_remote_storage_dir(thumbnails=True)
        thumbnails_dir = self.get_processing_dir(thumbnails=True)

        for filename in os.listdir(thumbnails_dir):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                file_path = os.path.join(thumbnails_dir, filename)
                public_url = upload_file(filename, file_path, remote_location)

                position = os.path.splitext(filename)[0]
                Thumbnail.objects.create(video=self, position=position, public_url=public_url)

    def delete_temp_files(self):
        shutil.rmtree(self.get_processing_dir())

    def delete_thumbnails(self):
        """
        This function deletes all the thumbnails associated with the video.
        """
        from core.models.thumbnail import Thumbnail
        Thumbnail.objects.filter(video=self).delete()
        shutil.rmtree(self.get_processing_dir(thumbnails=True))

    def remove_new_video_tag(self):
        """
        This function removes the "new video" tag from the video instance.
        """
        try:
            tag = Tag.objects.get(name=strings.Constant.NEW_VIDEO)
            self.tag.remove(tag)
            self.save()

        except Tag.DoesNotExist:
            pass

    def is_processing(self):
        """
        This function changes the status of the video to processing.
        """
        self.status = strings.Constant.PROCESSING
        self.save()

    def is_uploading(self):
        """
        This function changes the status of the video to uploading.
        """
        self.status = strings.Constant.UPLOADING
        self.save()

    def is_ready(self):
        """
        This function changes the status of the video to ready.
        """
        self.status = strings.Constant.READY
        self.save()

    def get_thumbnail_public_url(self, position=1):
        from .thumbnail import Thumbnail
        try:
            return Thumbnail.objects.get(video=self, position=position).public_url
        except Thumbnail.DoesNotExist:
            return None

    def get_processing_dir(self, thumbnails=False):
        """
        Get the directory that contains the video in HLS format and thumbnails.
        If thumbnails is True, it will return the location for thumbnails instead.
        """
        if thumbnails:
            return os.path.join(PROCESSING_DIR, str(self.id), 'thumbnails')

        return os.path.join(PROCESSING_DIR, str(self.id))

    def get_remote_storage_dir(self, thumbnails=False):
        """
        This is the location where the video is stored in at Google Cloud.
        If thumbnail is True, it will return the location for thumbnails instead.
        """
        path = 'videos/' + str(self.id)

        if thumbnails is True:
            path += '/thumbnails'

        return 'debug/' + path if settings.DEBUG else path

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Video)


# noinspection PyUnusedLocal
@receiver(post_save, sender=Video)
def process_video(sender, instance, created, **kwargs):
    assert isinstance(instance, Video)
    scheduler.run()

    if created:
        tag = Tag.objects.get_or_create(name=strings.Constant.NEW_VIDEO)[0]
        instance.tag.add(tag)
        instance.save()


# noinspection PyUnusedLocal
@receiver(pre_delete, sender=Video)
def delete_video(sender, instance, **kwargs):
    """
    This function deletes the video folder from the server.
    """
    delete_folder(instance.get_remote_storage_dir())
