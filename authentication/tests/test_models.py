import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestUser:
    def test_str_method(self):
        user = mixer.blend("authentication.User")
        assert hasattr(user, "__str__"), "User should have __str__ method"
        assert str(user), "Should return non-empty string"
