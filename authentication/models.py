from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import AbstractUser
from .constants import *


class User(AbstractUser):
    SHARE_TEXT = 'Account, with whom you want to share your accounting.'
    email = models.EmailField(
        unique=True,
        error_messages={'unique': USER_EMAIL_CONSTRAINT_MESSAGE}
    )
    image = models.TextField(null=True, blank=True, default=DEFAULT_USER_IMAGE) # Image is saved as base64 string
    slug = models.SlugField(max_length=200, blank=True)
    sharing_with = models.ManyToManyField(
        'self',
        symmetrical=True,
        related_name='sharing_users',
        related_query_name='sharing_query_user',
        help_text=SHARE_TEXT
    )

    def __str__(self):
        return f'{self.email}, {self.username}'

    @staticmethod
    def get_by_username(username):
        return User.objects.filter(username=username).first()

    @staticmethod
    def get_by_email(email):
        return User.objects.filter(email=email).first()

    @staticmethod
    def get_bu_credentials(username, email):
        return User.objects.filter(
            models.Q(username=username) | models.Q(email=email)).first()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.username)
        return super().save(*args, **kwargs)
