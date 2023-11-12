""" File with helper functions """

import random
import string
from webhelpers.settings import ALIAS_LENGTH
from urlshortener.models import LinkPair


def alias_generator(length: int = ALIAS_LENGTH) -> str:
    """
    The function generates a random alias of characters with a specified length and checks if it
    already exists in the database, generating a new one if necessary.

    :param length: The "length" parameter is an optional parameter that specifies the length of the
    generated alias. If no value is provided, it will default to the value of the constant
    "ALIAS_LENGTH"
    :type length: int
    :return: a randomly generated string of characters.
    """
    characters = string.ascii_letters + string.digits
    alias = ''.join(random.choice(characters) for _ in range(length))

    while LinkPair.objects.filter(alias=alias).exists():
        alias = alias_generator()

    return alias
