from django.core.exceptions import ValidationError
from django.test import TestCase

from core.models import Video, Thumbnail


class ThumbnailTestCase(TestCase):
    def setUp(self):
        self.video = Video.objects.create(name="Test video")
        Thumbnail.objects.create(video=self.video, position=1)

    def test_unique_constraint_1(self):
        # Arrange.
        thumbnail = Thumbnail(video=self.video, position=1)

        # Assert.
        self.assertRaises(ValidationError, thumbnail.save)

    def test_unique_constraint_2(self):
        # Arrange.
        thumbnail = Thumbnail(video=self.video, position=2)

        # Assert.
        self.assertTrue(True)
