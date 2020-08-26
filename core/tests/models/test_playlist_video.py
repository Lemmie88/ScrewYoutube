from django.test import TestCase

from core.models import Video, Playlist, PlaylistVideo


class PlaylistVideoTestCase(TestCase):
    def setUp(self):
        self.playlist_1 = Playlist.objects.create(name="Playlist 1")
        self.video_1 = Video.objects.create(name="Video 1")
        self.video_2 = Video.objects.create(name="Video 2")
        self.video_3 = Video.objects.create(name="Video 3")

    def test_get_latest_position_1(self):
        # Arrange.
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_1)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_2)

        # Act.
        position = Playlist.objects.get(name="Playlist 1").get_latest_position()

        # Assert.
        self.assertEqual(position, 2)

    def test_get_latest_position_2(self):
        # Arrange.
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_1)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_2)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_3)

        # Act.
        position = Playlist.objects.get(name="Playlist 1").get_latest_position()

        # Assert.
        self.assertEqual(position, 3)

    def test_get_latest_position_3(self):
        # Act.
        position = Playlist.objects.get(name="Playlist 1").get_latest_position()

        # Assert.
        self.assertEqual(position, 0)

    def test_get_video_position(self):
        # Arrange.
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_1)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_2)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_3)

        # Act.
        playlist = Playlist.objects.get(name="Playlist 1")
        position_1 = playlist.get_video_position(self.video_1)
        position_2 = playlist.get_video_position(self.video_2)
        position_3 = playlist.get_video_position(self.video_3)

        # Assert.
        self.assertEqual(position_1, 1)
        self.assertEqual(position_2, 2)
        self.assertEqual(position_3, 3)

    def test_get_videos(self):
        # Arrange.
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_3)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_2)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_1)

        # Act.
        playlist = Playlist.objects.get(name="Playlist 1")
        videos = playlist.get_videos()

        # Assert.
        self.assertEqual(videos[0], self.video_3)
        self.assertEqual(videos[1], self.video_2)
        self.assertEqual(videos[2], self.video_1)

    def test_delete_video(self):
        # Arrange.
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_3)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_2)
        PlaylistVideo.objects.create(playlist=self.playlist_1, video=self.video_1)

        # Act.
        playlist = Playlist.objects.get(name="Playlist 1")
        playlist.delete_video(self.video_2)

        # Assert.
        self.assertEqual(playlist.get_video_position(self.video_3), 1)
        self.assertEqual(playlist.get_video_position(self.video_2), None)
        self.assertEqual(playlist.get_video_position(self.video_1), 2)

    def test_add_video(self):
        # Arrange.
        self.playlist_1.add_video(self.video_1)
        self.playlist_1.add_video(self.video_1)

        # Act.
        videos = self.playlist_1.get_videos()

        # Assert.
        self.assertEqual(len(videos), 1)
        self.assertEqual(videos[0], self.video_1)
