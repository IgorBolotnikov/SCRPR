from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from authentication.constants import *


class User(AbstractUser):
    email = models.EmailField(
        unique=True,
        error_messages={'unique': USER_EMAIL_CONSTRAINT_MESSAGE}
    )
    image = models.TextField(null=True, blank=True, default=DEFAULT_USER_IMAGE) # Image is saved as base64 string

    def __str__(self):
        return f'{self.email}, {self.username}'
