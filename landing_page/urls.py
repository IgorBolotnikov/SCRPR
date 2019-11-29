from django.urls import path
from .views import MainContactView

app_name = 'landing_page'
urlpatterns = [
    path('', MainContactView.as_view(), name='index'),
]
