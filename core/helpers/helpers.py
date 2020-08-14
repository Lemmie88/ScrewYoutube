import random
import string

import core.strings as strings

LENGTH = strings.Constants.DEFAULT_CODE_LENGTH


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
