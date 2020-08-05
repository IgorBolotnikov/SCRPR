from django.contrib import admin

from .models import Comment, FavoriteGameQuery, FavoriteJobQuery, NewsPost

# Register your models here.
admin.site.register(Comment)
admin.site.register(NewsPost)
admin.site.register(FavoriteGameQuery)
admin.site.register(FavoriteJobQuery)
