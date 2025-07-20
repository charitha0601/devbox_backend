import pytest
from django.urls import reverse
from rest_framework.test import APIClient
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import datetime, timezone

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def test_user(db):
    user = User.objects.create_user(username='devbox', password='Devbox@123')
    return user

@pytest.fixture
def auth_headers(test_user):
    refresh = RefreshToken.for_user(test_user)
    access = str(refresh.access_token)
    print(f"Generated access token: {access}")
    return {"HTTP_AUTHORIZATION": f"Bearer {access}"}

def test_login_success(api_client, test_user):
    url = reverse('token_obtain_pair')
    data = {"username": "devbox", "password": "Devbox@123"}
    response = api_client.post(url, data)
    assert response.status_code == 200
    assert "access" in response.data

def test_profile_authenticated(api_client, auth_headers):
    url = reverse('profile')
    response = api_client.get(url, **auth_headers)
    assert response.status_code == 200
    assert response.data['username'] == "devbox"  # based on MOCK data

def test_profile_unauthenticated(api_client):
    url = reverse('profile')
    response = api_client.get(url)
    assert response.status_code == 401

def test_get_api_usage_authenticated(api_client, auth_headers):
    url = reverse('api-usage')
    response = api_client.get(url, **auth_headers)
    assert response.status_code == 200
    assert isinstance(response.data, list)

def test_post_api_usage_success(api_client, auth_headers):
    url = reverse('api-usage')
    data = {
        "endpoint": "/test-endpoint",
        "method": "POST",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    response = api_client.post(url, data, format='json', **auth_headers)
    assert response.status_code == 201
    assert response.data['message'] == "API usage logged successfully."

def test_post_api_usage_invalid_data(api_client, auth_headers):
    url = reverse('api-usage')
    data = {
        "endpoint": "/test-endpoint",
        "method": "POST"
        # missing timestamp
    }
    response = api_client.post(url, data, format='json', **auth_headers)
    assert response.status_code == 400
