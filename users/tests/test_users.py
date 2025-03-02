import pytest
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token


@pytest.mark.django_db
class TestCustomTelegramUserModel:
    @pytest.fixture
    def user_data(self):
        user = get_user_model().objects.create_user(
            username='testuser',
            password='password',
        )
        return user

    def test_user_creation(self, user_data):
        user = user_data
        assert user.username == 'testuser'
        assert user.check_password('password')

    def test_user_is_employee_default(self, user_data):
        user = user_data
        assert not user.is_employee

    def test_check_user_token(self, user_data):
        user = user_data
        assert Token.objects.filter(user=user).exists()
