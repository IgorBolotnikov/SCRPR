from django.urls import path, re_path

from api_v1.views import *

app_name = 'api_v1'

urlpatterns = [
    path('news', NewsListView.as_view(), name='news-list'),
]
