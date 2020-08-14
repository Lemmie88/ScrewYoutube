from django.core.exceptions import ValidationError
from django.test import TestCase

import core.strings as strings
from core.models import Playlist


class PlaylistTestCase(TestCase):
    def setUp(self):
        Playlist.objects.create(name="Test 1")

    def test_url_is_generated(self):
        # Act.
        code = Playlist.objects.get(name="Test 1").url

        # Assert.
        self.assertEqual(len(code), strings.Constants.DEFAULT_CODE_LENGTH)

    def test_url_is_unique(self):
        # Arrange.
        code = Playlist.objects.get(name="Test 1").url

        # Act.
        playlist = Playlist(name="Test 2", url=code)

        # Assert.
        self.assertRaises(ValidationError, playlist.save)

    def test_url_is_same(self):
        # Arrange.
        playlist = Playlist.objects.get(name="Test 1")
        code = playlist.url

        # Act.
        playlist.name = "Test 2"
        playlist.save()

        # Assert.
        self.assertEqual(code, Playlist.objects.get(name="Test 2").url)
