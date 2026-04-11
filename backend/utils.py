from django.conf import settings
from django.utils.text import slugify
from django.utils.crypto import get_random_string


def generate_slug(text: str, *, max_length: int = settings.DEFAULT_SLUG_SIZE) -> str:
    """
    A generic slug generator that creates a slug from the given text and appends a random string to ensure uniqueness.
    """
    return f'{slugify(text)[: max_length - 4]}-{get_random_string(4)}'
