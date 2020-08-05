from django.db import models

from authentication.models import User


class SavedSuggestion(models.Model):
    SUGGESITION_JOB = "JOB"
    SUGGESTION_GAME = "GAME"

    SUCCESTION_TYPES = [
        (SUGGESITION_JOB, "Job"),
        (SUGGESTION_GAME, "Game"),
    ]

    saved_datetime = models.DateTimeField(auto_now_add=True)
    type = models.CharField(max_length=10, choices=SUCCESTION_TYPES)
    link = models.URLField(max_length=500)
    account = models.ForeignKey(
        User,
        related_name="suggestions",
        related_query_name="suggestion",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Suggestion for {self.account.username}"
