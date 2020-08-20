from core.helpers.helper import generate_url_code
from core.models.base import BaseModel


class Playlist(BaseModel):
    class Meta:
        ordering = ["name"]
        get_latest_by = ["-date_modified"]

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Playlist)
