from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Job)
admin.site.register(Game)
admin.site.register(Comment)
admin.site.register(NewsPost)
admin.site.register(FavoriteGameQuery)
admin.site.register(FavoriteJobQuery)
