from django import forms

from core import strings
from core.helpers.form import Form
from core.models import Playlist


class AddPlaylistForm(forms.Form):
    title = forms.CharField(
        max_length=250
    )

    description = forms.CharField(
        required=False
    )

    def clean(self):
        cleaned_data: dict = super().clean()

        # Checks whether playlist title is unique.
        title = Form.get_title(cleaned_data)
        playlist = Playlist.objects.filter(name=title)
        if playlist.exists():
            self._errors[strings.Form.TITLE] = self.error_class([strings.Error.UNUNIQUE_PLAYLIST_TITLE])
