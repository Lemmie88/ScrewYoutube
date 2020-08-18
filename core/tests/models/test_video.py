from django.core.exceptions import ValidationError
from django.test import TestCase

import core.strings as strings
from core.models import Video


class VideoTestCase(TestCase):
    def setUp(self):
        Video.objects.create(name="Test 1")

    def test_url_is_generated(self):
        # Act.
        code = Video.objects.get(name="Test 1").url

        # Assert.
        self.assertEqual(len(code), strings.Constant.DEFAULT_CODE_LENGTH)

    def test_url_is_unique(self):
        # Arrange.
        code = Video.objects.get(name="Test 1").url

        # Act.
        video = Video(name="Test 2", url=code)

        # Assert.
        self.assertRaises(ValidationError, video.save)

    def test_url_is_same(self):
        # Arrange.
        video = Video.objects.get(name="Test 1")
        code = video.url

        # Act.
        video.name = "Test 2"
        video.save()

        # Assert.
        self.assertEqual(code, Video.objects.get(name="Test 2").url)
