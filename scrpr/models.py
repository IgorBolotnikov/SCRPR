from tinymce import models as tinymce_models

from django.db import models

from authentication.models import User

from .constants import (
    CHOICES_DICT,
    CITY_CHOICES,
    FREE_LABEL,
    INITIAL_PRICE_LABEL,
    NOTIFICATION_CHOICES,
    NUMERIC_MAX_LABEL,
    NUMERIC_MIN_LABEL,
    PSPLUS_PRICE_LABEL,
    WITH_SALARY_LABEL,
)


class Comment(models.Model):
    name = models.CharField(max_length=100)
    comment = models.TextField()
    datetime_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.name}"


class NewsPost(models.Model):
    title = models.CharField(max_length=200)
    body = tinymce_models.HTMLField()
    datetime_posted = models.DateTimeField()

    class Meta:
        ordering = ["-datetime_posted"]

    def __str__(self):
        return self.title


class FavoriteGameQuery(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    price_min = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    price_max = models.DecimalField(
        max_digits=9, decimal_places=2, null=True, blank=True
    )
    psplus_price = models.BooleanField(blank=True, default=False)
    initial_price = models.BooleanField(blank=True, default=False)
    free = models.BooleanField(blank=True, default=False)
    notification_freq = models.PositiveSmallIntegerField(
        choices=NOTIFICATION_CHOICES, null=True, blank=True
    )
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Favorite game queries"

    def __str__(self):
        return (
            f'Query: "{self.title}" by '
            f"{self.account.username}, {self.notification_freq}"
        )

    @property
    def details(self):
        details = ""
        details += (
            f", {NUMERIC_MIN_LABEL}: {self.price_min} UAH"
            if self.price_min
            else ""
        )
        details += (
            f", {NUMERIC_MAX_LABEL}: {self.price_max} UAH"
            if self.price_max
            else ""
        )
        details += f", {PSPLUS_PRICE_LABEL}" if self.psplus_price else ""
        details += f", {INITIAL_PRICE_LABEL}" if self.initial_price else ""
        details += f", {FREE_LABEL}." if self.free else ""
        return details

    @property
    def notification_frequency(self):
        return CHOICES_DICT[self.notification_freq]


class FavoriteJobQuery(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(
        max_length=50, choices=CITY_CHOICES, null=True, blank=True
    )
    salary_min = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    salary_max = models.DecimalField(
        max_digits=8, decimal_places=2, null=True, blank=True
    )
    with_salary = models.BooleanField(blank=True, default=False)
    notification_freq = models.PositiveSmallIntegerField(
        choices=NOTIFICATION_CHOICES, null=True, blank=True
    )
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name_plural = "Favorite job queries"

    def __str__(self):
        return f'Query: "{self.title}" by {self.account.username}'

    @property
    def details(self):
        details = ""
        details += f", {self.city}" if self.city else ""
        details += (
            f", {NUMERIC_MIN_LABEL}: {self.salary_min} UAH"
            if self.salary_min
            else ""
        )
        details += (
            f", {NUMERIC_MAX_LABEL}: {self.salary_max} UAH"
            if self.salary_max
            else ""
        )
        details += f", {WITH_SALARY_LABEL}." if self.with_salary else ""
        return details

    @property
    def notification_frequency(self):
        return CHOICES_DICT[self.notification_freq]
