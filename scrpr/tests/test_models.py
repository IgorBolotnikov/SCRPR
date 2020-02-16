import pytest
from mixer.backend.django import mixer

from scrpr.models import *


pytestmark = pytest.mark.django_db


class TestComment:
    def test_str_method(self):
        comment = mixer.blend('scrpr.Comment')
        assert hasattr(comment, '__str__'), \
            'Comment should have __str__ method'
        assert str(comment) != "", 'Should return non-empty string'


class TestFavoriteGameQuery:
    def test_str_method(self):
        query = mixer.blend('scrpr.FavoriteGameQuery')
        assert hasattr(query, '__str__'), \
            'Comment should have __str__ method'
        assert str(query) != "", 'Should return non-empty string'

    def test_notification_frequemcy_property(self):
        query = mixer.blend('scrpr.FavoriteGameQuery')
        assert hasattr(query, 'notification_frequency'), \
            'FavoriteGameQuery should have notification_frequency property'
        assert query.notification_frequency, 'Should return non-empty string'

    def test_details_property(self):
        query = mixer.blend('scrpr.FavoriteGameQuery')
        assert hasattr(query, 'details'), \
            'FavoriteGameQuery should have details property'


class TestFavoriteJobQuery:
    def test_str_method(self):
        query = mixer.blend('scrpr.FavoriteJobQuery')
        assert hasattr(query, '__str__'), \
            'Comment should have __str__ method'
        assert str(query) != "", 'Should return non-empty string'

    def test_notification_frequemcy_property(self):
        query = mixer.blend('scrpr.FavoriteJobQuery')
        assert hasattr(query, 'notification_frequency'), \
            'FavoriteJobQuery should have notification_frequency property'
        assert query.notification_frequency, 'Should return non-empty string'

    def test_details_property(self):
        query = mixer.blend('scrpr.FavoriteJobQuery')
        assert hasattr(query, 'details'), \
            'FavoriteJobQuery should have details property'


class TestNewsPost:
    def test_str_method(self):
        post = mixer.blend('scrpr.NewsPost')
        assert hasattr(post, '__str__'), \
            'NewsPost should have __str__ method'
        assert str(post) != "", 'Should return non-empty string'
