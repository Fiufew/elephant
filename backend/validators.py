import os

from django.conf import settings


def contains_digits(s):
    return any(char.isdigit() for char in s)


def other_files_path(instance, filename):
    folder = os.path.join(
        settings.MEDIA_ROOT, f"other_files/Заявка_{instance.bid_id}")
    os.makedirs(folder, exist_ok=True)
    return f'other_files/Заявка_{instance.bid_id}/{filename}'
