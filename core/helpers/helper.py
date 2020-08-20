import random
import string

from faker import Faker

import core.strings as strings
from ScrewYoutube import settings

LENGTH = strings.Constant.DEFAULT_CODE_LENGTH


def generate_code(length=LENGTH) -> str:
    """
    This function generates a code of a certain length.
    :param length: Length of code
    """
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for _ in range(length))


def generate_url_code(model_class, length=LENGTH) -> str:
    """
    This function checks to ensure that the generated code is unique for the model.
    :param model_class: Class of model
    :param length: Length of code
    """
    while True:
        code = generate_code(length)
        if model_class.objects.filter(url=code).exists() is False:
            return code


def random_colour():
    """
    This function generates a random bright colour.
    """
    fake = Faker()
    return fake.color(luminosity='bright')


def get_context(page: strings.Page):
    """
    This function returns the base context required for all pages.
    """
    return {'debug': settings.DEBUG, 'strings': strings, 'page': page}
