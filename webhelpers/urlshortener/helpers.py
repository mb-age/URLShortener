""" File with helper functions """

import random
import string
from webhelpers.webhelpers.settings import LINK_LENGTH


def link_generator(length=LINK_LENGTH):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
