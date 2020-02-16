from django.urls import path, re_path, include

from rest_framework.routers import DefaultRouter

from api_v1.views import *
from authentication.api_views import *


router = DefaultRouter()
router.register(r'games', FavoritesGamesListView, basename='games')
router.register(r'jobs', FavoritesJobsListView, basename='jobs')

app_name = 'api_v1'
urlpatterns = [
    path('news', NewsListView.as_view(), name='news-list'),
    path('rate', CommentView.as_view(), name='rate'),
    path('favorites/', include(router.urls)),
    re_path(r'^api/v1/games$', GamesAPIView.as_view(), name='games_api'),
    re_path(r'^api/v1/jobs$', JobsAPIView.as_view(), name='jobs_api'),

    # From authentication app 'api_views.py'
    path('user', UserView.as_view(), name='user'),
    path('user/create', CreateUserView.as_view(), name='create-user'),
    path(
        'user/update-password',
        UpdatePasswordView.as_view(),
        name='update-password'
    )
]
