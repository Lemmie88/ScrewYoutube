from core import strings


class Form:
    @staticmethod
    def get_title(cleaned_data: dict) -> str:
        return cleaned_data.get(strings.Form.TITLE)

    @staticmethod
    def get_description(cleaned_data: dict) -> str:
        return cleaned_data.get(strings.Form.DESCRIPTION)
