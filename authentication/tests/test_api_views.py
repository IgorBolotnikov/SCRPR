import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import AnonymousUser
from authentication import api_views

from authentication.models import User


pytestmark = pytest.mark.django_db


class TestUserView:
    def test_get_response_for_anonymous_user(self):
        request = APIRequestFactory().get('/')
        request.user = AnonymousUser()
        response = api_views.UserView.as_view()(request)
        assert response.status_code == 401, \
            'Should not be accessible by anonymous users'

    def test_get_response_for_authenticated_user(self):
        request = APIRequestFactory().get('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.UserView.as_view()(request)
        assert response.status_code == 200, \
            'Should be accessible only by authenticated users'

    def test_response_content(self):
        request = APIRequestFactory().get('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.UserView.as_view()(request)
        assert response.data['username'] == request.user.username, \
            'Should return User data of a user, who have sent a request'

    def test_post_method_not_allowed(self):
        request = APIRequestFactory().post('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.UserView.as_view()(request)
        assert response.status_code == 405, 'Should not accept POST requests'

    def test_put_method(self):
        post_body = {
            "username": "testusername",
            "email": "testemail@testemail.com",
        }
        request = APIRequestFactory().put('/', post_body)
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.UserView.as_view()(request)
        data = response.data
        assert response.status_code == 200, 'Should return 200 OK response'
        assert data['username'] == post_body['username'], \
            'Should update username'
        assert data['email'] == post_body['email'], \
            'Should update email'

    def test_delete_method(self):
        request = APIRequestFactory().delete('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = api_views.UserView.as_view()(request)
        remaining_users = User.objects.all()
        assert response.status_code == 200, 'Should return 200 OK'
        assert not remaining_users, 'Should delete user'

class TestCreateUserView:
    def test_get_response(self):
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
        assert response.status_code == 201, \
            'Should successfully create new user'
        assert response.data.get('token') is not None, \
            'Should return JWT together with user data'
        assert 'password' not in response.data.keys(), \
            'Should not return password to user'

    def test_invalid_form_bad_request(self):
        post_body = {
            "username": "",
            "email": "incalidemail",
            "password": "short"
        }
        request = APIRequestFactory().post('/', post_body)
        request_user = AnonymousUser()
        response = api_views.CreateUserView.as_view()(request)
        assert response.status_code == 400, \
            'Should return 400: Bad request if user have sent invalid data'


class TestUpdatePasswordView:
    def test_put_response_for_anonymous_user(self):
        request = APIRequestFactory().put('/')
        request.user = AnonymousUser()
        response = api_views.UpdatePasswordView.as_view()(request)
        assert response.status_code == 401, \
            'Should be accessible only by authorized users'

    def test_valid_password_response(self):
        password = 'securepassword'
        user = mixer.blend('authentication.User')
        user.set_password(password)
        request = APIRequestFactory().put('/', {
            'old_password': password,
            'new_password': 'anotherpassword'
        })
        force_authenticate(request, user=user)
        response = api_views.UpdatePasswordView.as_view()(request)
        assert not response.data, 'Should not return any data'
        assert response.status_code == 200, 'Should return 200 OK'

    def test_invalid_password_response(self):
        user = mixer.blend('authentication.User', password='securepassword')
        request = APIRequestFactory().put('/', {
            'old_password': 'wrongpassword',
            'new_password': 'anotherpassword'
        })
        force_authenticate(request, user=user)
        response = api_views.UpdatePasswordView.as_view()(request)
        assert response.status_code == 400, 'Should return 400 BAD REQUEST'
        assert response.data, 'Should return error message'
