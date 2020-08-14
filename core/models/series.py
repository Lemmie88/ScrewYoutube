from core.helpers.helpers import generate_url_code
from core.models.base import BaseModel


class Series(BaseModel):
    class Meta:
        verbose_name = "Series"
        verbose_name_plural = "Series"
        ordering = ["name"]

    def clean(self):
        # Generate unique url code.
        if self.url is '' or self.url is None:
            self.url = generate_url_code(Series)
