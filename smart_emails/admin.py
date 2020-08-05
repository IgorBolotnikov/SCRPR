from django.contrib import admin

from .models import SavedSuggestion


class SavedSuggestionAdmin(admin.ModelAdmin):
    list_display = ["saved_datetime", "type", "link", "account"]


admin.site.register(SavedSuggestion, SavedSuggestionAdmin)
