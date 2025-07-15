import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from unittest.mock import patch
import bcrypt

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def mock_firebase_service():
    with patch('backend_project.firebase_service.firebase_service') as mock:
        yield mock

@pytest.mark.django_db
class TestAuthEndpoints:

    def test_register_success(self, api_client, mock_firebase_service):
        url = reverse('register')
        
        # Mockear Firebase para que no encuentre un usuario existente
        mock_firebase_service.get_user_by_email.return_value = None
        
        # Mockear la creación de usuario
        created_user = {
            'id': 'some-firebase-uid',
            'name': 'Test User',
            'email': 'test@example.com',
            'is_active': True
        }
        mock_firebase_service.create_user.return_value = created_user
        
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_201_CREATED
        assert 'user' in response.data
        assert 'tokens' in response.data
        assert response.data['user']['email'] == 'test@example.com'
        mock_firebase_service.create_user.assert_called_once()

    def test_register_password_mismatch(self, api_client):
        url = reverse('register')
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'confirm_password': 'wrongpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data or 'detail' in response.data

    def test_register_email_exists(self, api_client, mock_firebase_service):
        url = reverse('register')
        
        # Mockear Firebase para que encuentre un usuario existente
        mock_firebase_service.get_user_by_email.return_value = {'id': 'some-id', 'email': 'test@example.com'}
        
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'testpassword123',
            'confirm_password': 'testpassword123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'email' in response.data

    def test_login_success(self, api_client, mock_firebase_service):
        url = reverse('login')
        
        hashed_password = bcrypt.hashpw(b'testpassword123', bcrypt.gensalt()).decode('utf-8')
        
        # Mockear Firebase para que encuentre un usuario
        mock_user = {
            'id': 'some-firebase-uid',
            'name': 'Test User',
            'email': 'test@example.com',
            'password': hashed_password,
            'is_active': True
        }
        mock_firebase_service.get_user_by_email.return_value = mock_user
        
        data = {
            'email': 'test@example.com',
            'password': 'testpassword123'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_200_OK
        assert 'user' in response.data
        assert 'tokens' in response.data
        assert response.data['user']['email'] == 'test@example.com'

    def test_login_invalid_credentials(self, api_client, mock_firebase_service):
        url = reverse('login')
        
        # Mockear Firebase para que no encuentre un usuario
        mock_firebase_service.get_user_by_email.return_value = None
        
        data = {
            'email': 'wrong@example.com',
            'password': 'wrongpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data or 'detail' in response.data

    def test_login_wrong_password(self, api_client, mock_firebase_service):
        url = reverse('login')
        
        hashed_password = bcrypt.hashpw(b'testpassword123', bcrypt.gensalt()).decode('utf-8')
        
        # Mockear Firebase para que encuentre un usuario
        mock_user = {
            'id': 'some-firebase-uid',
            'name': 'Test User',
            'email': 'test@example.com',
            'password': hashed_password,
            'is_active': True
        }
        mock_firebase_service.get_user_by_email.return_value = mock_user
        
        data = {
            'email': 'test@example.com',
            'password': 'wrongpassword'
        }
        
        response = api_client.post(url, data, format='json')
        
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'non_field_errors' in response.data or 'detail' in response.data
