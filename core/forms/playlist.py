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
        playlist = Playlist.objects.filter(name__iexact=title)
        if playlist.exists():
            self._errors[strings.Form.TITLE] = self.error_class([strings.Error.UNUNIQUE_PLAYLIST_TITLE])


class EditPlaylistForm(forms.Form):
    playlist = forms.CharField(
        max_length=strings.Constant.DEFAULT_CODE_LENGTH
    )

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

        # Check if the title belongs to the playlist itself.
        if Playlist.objects.filter(url=cleaned_data.get('playlist'), name__iexact=title).exists() is False:
            if Playlist.objects.filter(name__iexact=title).exists():
                self._errors[strings.Form.TITLE] = self.error_class([strings.Error.UNUNIQUE_PLAYLIST_TITLE])
