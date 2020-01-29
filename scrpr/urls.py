from django.urls import path, re_path
from .views import *
from .api import *

app_name = 'scrpr'
urlpatterns = [

    # Regular URLs
    path('', MainPageView.as_view(), name='index'),
    path('news', NewsListView.as_view(), name='news'),
    path('favorites', FavoritesView.as_view(), name='favorites_list'),
    path('favorites/games/<int:pk>', FavoritesGameDetailView.as_view(), name='favorites_game'),
    path('favorites/games/<int:pk>/delete', FavoritesGameDeleteView.as_view(), name='favorites_game_delete'),
    path('favorites/jobs/<int:pk>', FavoritesJobDetailView.as_view(), name='favorites_job'),
    path('favorites/jobs/<int:pk>/delete', FavoritesJobDeleteView.as_view(), name='favorites_job_delete'),
    path('logout', CustomLogoutView.as_view(), name='logout'),
    path('about', AboutView.as_view(), name='about'),
    path('rate', RateView.as_view(), name='rate'),
    re_path(r'^games$', GamesView.as_view(), name='games'),
    re_path(r'^jobs$', JobsView.as_view(), name='jobs'),
    path('freelance', freelance, name='freelance'),

    # REST API
    re_path(r'^api/games$', GamesAPIView.as_view(), name='games'),
]
