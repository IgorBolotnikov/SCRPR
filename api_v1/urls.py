from django.urls import path, re_path

from api_v1.views import *
from authentication.api_views import *

app_name = 'api_v1'

urlpatterns = [
    path('news', NewsListView.as_view(), name='news-list'),
    path('favorites/games', FavoritesGamesListView.as_view()),
    path('favorites/jobs', FavoritesJobsListView.as_view()),

    path('user', UserView.as_view(), name='user'),
    path('user/create', CreateUserView.as_view(), name='create-user'),
]
