import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate
from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from api_v1 import views


pytestmark = pytest.mark.django_db


@pytest.mark.django_db
class PaginationMixin:
    '''
    When inheriting this mixin the followng class attrs need to be set up:
    model_class (string of format 'app_name.model_class')
    view_class (view class)
    authenticate = (bool)
    models_owner = (bool)
    objects_num = (int)
    viewset = (bool)
    viewset_method (only if viewset = True,
                    dict of format {'HTTP_method': 'ViewSet_method'})
    '''
    page_size = settings.REST_FRAMEWORK['PAGE_SIZE']

    def test_paginated_results(self):
        request = APIRequestFactory().get('/')
        # Conditional user authentication
        if self.authenticate:
            user = mixer.blend('authentication.User')
            force_authenticate(request, user=user)
        else:
            user = AnonymousUser()
        # Conditional assignment of User instance to mixer objects
        if self.models_owner:
            objects = mixer.cycle(self.objects_num).blend(
                self.model_class,
                account=user
            )
        else:
            objects = mixer.cycle(self.objects_num).blend(self.model_class)
        obj_name = self.model_class.split('.')[1]
        last_page = int(self.objects_num / self.page_size)
        # Conditional addition of specific viewset method
        if self.viewset:
            response = self.view_class.as_view(self.viewset_method)(request)
        else:
            response = self.view_class.as_view()(request)
        pagination = response.data.get('pagination')
        results = response.data.get('results')
        assert response.status_code == 200, 'Should be accessible by anyone'
        assert results, 'Should return %s results' % obj_name
        assert len(results) == self.page_size, \
            'Should return last %s %s objects' % (self.page_size, obj_name)
        assert pagination, 'Pagination should be in response data'
        assert pagination['page'] == 1, 'Should return first page by default'
        assert pagination['prev_page'] == None, 'Should not have previous page'
        assert pagination['next_page'] == 2, 'Should have next page'
        assert pagination['last_page'] == last_page, \
            'Last page should be %s' % last_page
        assert pagination['page_size'] == self.page_size, \
            'Page size should be %s' % self.page_size


class TestNewsView(PaginationMixin):
    model_class = 'scrpr.NewsPost'
    view_class = views.NewsListView
    authenticate = True
    models_owner = False
    objects_num = 40
    viewset = False

    # def test_get_response(self):
    #     request = APIRequestFactory().get('/')
    #     news = mixer.cycle(40).blend('scrpr.NewsPost')
    #     response = views.NewsListView.as_view()(request)
    #     pagination = response.data.get('pagination')
    #     results = response.data.get('results')
    #     assert response.status_code == 200, 'Should be accessible by anyone'
    #     assert results, 'Should return News results'
    #     assert len(results) == 10, 'Should return last 10 News'
    #     assert pagination, 'Pagination should be in response data'
    #     assert pagination['page'] == 1, 'Should return first page by default'
    #     assert pagination['prev_page'] == None, 'Should not have previous page'
    #     assert pagination['next_page'] == 2, 'Should have next page'
    #     assert pagination['last_page'] == 4, 'Should have correct last page'
    #     assert pagination['page_size'] == 10, 'Page size should be 10'


class TestFavoritesGamesListView(PaginationMixin):
    model_class = 'scrpr.FavoriteGameQuery'
    view_class = views.FavoritesGamesListView
    authenticate = True
    models_owner = True
    objects_num = 20
    viewset = True
    viewset_method = {'get': 'list'}

    def test_get_response_for_anonymous_user(self):
        request = APIRequestFactory().get('/')
        request.user = AnonymousUser()
        response = self.view_class.as_view(self.viewset_method)(request)
        assert response.status_code == 401, \
            'Should not be accessible by anonymous users'


    def test_get_response_for_authenticated_user(self):
        request = APIRequestFactory().get('/')
        user = mixer.blend('authentication.User')
        force_authenticate(request, user=user)
        response = self.view_class.as_view(self.viewset_method)(request)
        assert response.status_code == 200, \
            'Should be accessible only by authenticated users'
