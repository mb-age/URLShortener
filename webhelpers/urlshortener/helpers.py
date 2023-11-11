""" File with helper functions """

import random
import string
from webhelpers.settings import LINK_LENGTH


def link_generator(length: int = LINK_LENGTH) -> str:
    """
    The function generates a random string of characters with a specified length.

    :param length: The length parameter is the length of the generated link. It is an optional parameter
    with a default value of LINK_LENGTH
    :return: a randomly generated string of characters with a length specified by the `length`
    parameter.
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
