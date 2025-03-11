from django.core.exceptions import ValidationError
from django.utils import timezone


def validate_manufactured_year(value):
    if value > timezone.now().year:
        raise ValidationError(
            'Year manufactured cannot be in the future'
        )
