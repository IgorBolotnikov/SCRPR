import pytest
from mixer.backend.django import mixer
from rest_framework.test import APIRequestFactory, force_authenticate
from django.contrib.auth.models import AnonymousUser
from api_v1 import views


pytestmark = pytest.mark.django_db


class TestNewsView:
    def test_get_response(self):
        request = APIRequestFactory().get('/')
        news = mixer.cycle(40).blend('scrpr.NewsPost')
        response = views.NewsListView.as_view()(request)
        pagination = response.data.get('pagination')
        results = response.data.get('results')
        assert response.status_code == 200, 'Should be accessible by anyone'
        assert results, 'Should return News results'
        assert len(results) == 10, 'Should return last 10 News'
        assert pagination, 'Pagination should be in response data'
        assert pagination['page'] == 1, 'Should return first page by default'
        assert pagination['prev_page'] == None, 'Should not have previous page'
        assert pagination['next_page'] == 2, 'Should have next page'
        assert pagination['last_page'] == 4, 'Should have correct last page'
        assert pagination['page_size'] == 10, 'Page size should be 10'
