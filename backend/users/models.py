from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework.authtoken.models import Token


class CustomElephantUser(AbstractUser):
    is_employee = models.BooleanField(
        default=False
    )

    def save(self, *args, **kwargs):
        created = not self.pk
        super().save(*args, **kwargs)
        if created:
            Token.objects.create(user=self)
