from django.contrib.auth.models import AbstractUser
from django.db import models

from authentication.constants import (
    DEFAULT_USER_IMAGE,
    USER_EMAIL_CONSTRAINT_MESSAGE,
)


class User(AbstractUser):
    email = models.EmailField(
        unique=True, error_messages={"unique": USER_EMAIL_CONSTRAINT_MESSAGE}
    )
    # Image is saved as base64 string
    image = models.TextField(null=True, blank=True, default=DEFAULT_USER_IMAGE)

    def __str__(self):
        return f"{self.email}, {self.username}"
