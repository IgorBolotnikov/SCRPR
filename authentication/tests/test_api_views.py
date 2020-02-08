import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import AnonymousUser
from authentication import api_views


pytestmark = pytest.mark.django_db


class TestRetrieveUserView:
    def test_get_response_for_anonymous_user(self):
        request = APIRequestFactory().get('/')
        request.user = AnonymousUser()
        response = api_views.RetrieveUserView.as_view()(request)
        assert response.status_code == 401, ('Should not be accessible '
                                             'by anonymous users')

    def test_get_response_for_authenticated_user(self):
        request = APIRequestFactory().get('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.RetrieveUserView.as_view()(request)
        assert response.status_code == 200, ('Should be accessible only '
                                             'by authenticated users')

    def test_response_content(self):
        request = APIRequestFactory().get('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.RetrieveUserView.as_view()(request)
        assert response.data['username'] == request.user.username, (
            'Should return User data of a user, who have sent a request')

    def test_post_method_not_allowed(self):
        request = APIRequestFactory().post('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.RetrieveUserView.as_view()(request)
        assert response.status_code == 405, ('Should not accept POST requests')


class TestCreateUserView:
    def test_get_response_for_anonymous_user(self):
        request = APIRequestFactory().get('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.CreateUserView.as_view()(request)
        assert response.status_code == 405, 'GET method should not be allowed'

    def test_user_creation(self):
        post_body = {
            "username": "testusername",
            "email": "testemail@testemail.com",
            "password": "securepassword"
        }
        request = APIRequestFactory().post('/', post_body)
        request.user = AnonymousUser()
        response = api_views.CreateUserView.as_view()(request)
        assert response.status_code == 201, ('Should successfully '
                                             'create new user')
        assert response.data.get('token') is not None, ('Should return JWT '
                                                        'together with '
                                                        'user data')
        assert 'password' not in response.data.keys(), ('Should not return '
                                                        'password to user')

    def test_invalid_form_bad_request(self):
        post_body = {
            "username": "",
            "email": "incalidemail",
            "password": "short"
        }
        request = APIRequestFactory().post('/', post_body)
        request_user = AnonymousUser()
        response = api_views.CreateUserView.as_view()(request)
        assert response.status_code == 400, ('Should return 400: Bad request '
                                             'if user have sent invalid data')
