import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory
from django.contrib.auth.models import AnonymousUser
from authentication import api_views
from rest_framework_jwt.views import refresh_jwt_token


pytestmark = pytest.mark.django_db


class TestJWTView:
    def test_post_response(self):
        post_body = {
            'username': 'username',
            'email': 'validemail@validddomain.com',
            'password': 'securepassword'
        }
        request = APIRequestFactory().post('/', post_body, format='json')
        request.user = AnonymousUser()
        response = api_views.CreateUserView.as_view()(request)
        token = response.data['token']
        request = APIRequestFactory().post('/', {'token': token})
        request.user = AnonymousUser()
        response = refresh_jwt_token(request)
        assert response.status_code == 200, 'Should return 200 OK'
        assert response.data.get('token'), 'Should return refreshed token'
        assert response.data.get('user'), 'Should return user data'
        assert response.data.get('user')['username'] == 'username', \
            'Should return the same user data'
