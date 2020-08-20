from django import forms


class EditVideoForm(forms.Form):
    title = forms.CharField(
        max_length=250
    )

    description = forms.CharField(
        required=False
    )
