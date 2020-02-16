import pytest
from mixer.backend.django import mixer


pytestmark = pytest.mark.django_db


class TestSavedSuggestion:
    def test_str_method(self):
        suggestion = mixer.blend('smart_emails.SavedSuggestion')
        assert hasattr(suggestion, '__str__'), \
            'SavedSuggestion should have __str__ method'
        assert str(suggestion), 'Should return non-empty string'
