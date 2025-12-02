"""Tests for the accounts application."""

import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from django.core.files.uploadedfile import SimpleUploadedFile
from PIL import Image
import io

from accounts.forms import UserRegistrationForm, UserProfileForm
from accounts.models import UserProfile

User = get_user_model()


class AccountsViewsTestCase(TestCase):
    """Test cases for accounts views."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
        
        self.admin_user = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="adminpass123",
            first_name="Admin",
            last_name="User"
        )
    
    def test_login_view_get(self):
        """Test login view GET request."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AuthenticationForm)
    
    def test_login_view_post_valid(self):
        """Test login view POST request with valid credentials."""
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after login
        
        # Check if user is logged in
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
    
    def test_login_view_post_invalid(self):
        """Test login view POST request with invalid credentials."""
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(reverse('accounts:login'), data)
        self.assertEqual(response.status_code, 200)  # Stay on page with errors
        self.assertContains(response, 'Please enter a correct username and password')
    
    def test_register_view_get(self):
        """Test register view GET request."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserRegistrationForm)
    
    def test_register_view_post_valid(self):
        """Test register view POST request with valid data."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123'
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after registration
        
        # Check if user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_register_view_post_invalid(self):
        """Test register view POST request with invalid data."""
        data = {
            'username': 'testuser',  # Already exists
            'email': 'invalid-email',
            'first_name': '',
            'last_name': '',
            'password1': 'pass',  # Too short
            'password2': 'different'  # Doesn't match
        }
        response = self.client.post(reverse('accounts:register'), data)
        self.assertEqual(response.status_code, 200)  # Stay on page with errors
        self.assertFormError(response, 'form', 'username', 'A user with that username already exists.')
    
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['user'], self.user)
    
    def test_profile_view_anonymous(self):
        """Test profile view for anonymous user."""
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_profile_edit_view_get(self):
        """Test profile edit view GET request."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:profile_edit'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], UserProfileForm)
    
    def test_profile_edit_view_post_valid(self):
        """Test profile edit view POST request with valid data."""
        self.client.force_login(self.user)
        data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'bio': 'Updated bio',
            'location': 'Updated Location',
            'website': 'https://updated.com',
            'github_url': 'https://github.com/updated',
            'linkedin_url': 'https://linkedin.com/in/updated',
            'twitter_url': 'https://twitter.com/updated'
        }
        response = self.client.post(reverse('accounts:profile_edit'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after update
        
        # Check if user was updated
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Updated')
        self.assertEqual(self.user.email, 'updated@example.com')
    
    def test_dashboard_view_authenticated(self):
        """Test dashboard view for authenticated user."""
        self.client.force_login(self.user)
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_dashboard_view_anonymous(self):
        """Test dashboard view for anonymous user."""
        response = self.client.get(reverse('accounts:dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect to login
    
    def test_logout_view(self):
        """Test logout view."""
        self.client.force_login(self.user)
        response = self.client.post(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)  # Redirect after logout


class UserProfileModelTestCase(TestCase):
    """Test cases for UserProfile model."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
    
    def test_user_profile_creation(self):
        """Test user profile is created automatically."""
        # Profile should be created automatically via signal
        self.assertTrue(hasattr(self.user, 'profile'))
        self.assertIsInstance(self.user.profile, UserProfile)
    
    def test_user_profile_str_representation(self):
        """Test user profile string representation."""
        expected_str = f"{self.user.get_full_name()} Profile"
        self.assertEqual(str(self.user.profile), expected_str)
    
    def test_user_profile_get_absolute_url(self):
        """Test user profile get_absolute_url method."""
        expected_url = reverse('accounts:profile')
        self.assertEqual(self.user.profile.get_absolute_url(), expected_url)
    
    def test_user_profile_avatar_upload(self):
        """Test user profile avatar upload."""
        # Create a test image
        image = Image.new('RGB', (100, 100), color='red')
        image_file = io.BytesIO()
        image.save(image_file, 'JPEG')
        image_file.seek(0)
        
        uploaded_file = SimpleUploadedFile(
            "test_avatar.jpg",
            image_file.getvalue(),
            content_type="image/jpeg"
        )
        
        self.user.profile.avatar = uploaded_file
        self.user.profile.save()
        
        self.assertTrue(self.user.profile.avatar)
        self.assertIn('avatars/', self.user.profile.avatar.name)


class UserRegistrationFormTestCase(TestCase):
    """Test cases for UserRegistrationForm."""
    
    def test_registration_form_valid_data(self):
        """Test registration form with valid data."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_registration_form_password_mismatch(self):
        """Test registration form with password mismatch."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newuserpass123',
            'password2': 'differentpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)
    
    def test_registration_form_duplicate_username(self):
        """Test registration form with duplicate username."""
        # Create existing user
        User.objects.create_user(
            username='existinguser',
            email='existing@example.com',
            password='existingpass123'
        )
        
        form_data = {
            'username': 'existinguser',  # Duplicate
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_registration_form_save(self):
        """Test registration form save method."""
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123'
        }
        form = UserRegistrationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertIsInstance(user, User)
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertTrue(user.check_password('newuserpass123'))


class UserProfileFormTestCase(TestCase):
    """Test cases for UserProfileForm."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User"
        )
    
    def test_profile_form_valid_data(self):
        """Test profile form with valid data."""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'bio': 'Updated bio',
            'location': 'Updated Location',
            'website': 'https://updated.com',
            'github_url': 'https://github.com/updated',
            'linkedin_url': 'https://linkedin.com/in/updated',
            'twitter_url': 'https://twitter.com/updated'
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
    
    def test_profile_form_invalid_email(self):
        """Test profile form with invalid email."""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'invalid-email',
            'bio': 'Updated bio'
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_profile_form_invalid_urls(self):
        """Test profile form with invalid URLs."""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'website': 'invalid-url',
            'github_url': 'not-a-url',
            'linkedin_url': 'also-not-a-url'
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)
        self.assertIn('github_url', form.errors)
        self.assertIn('linkedin_url', form.errors)
    
    def test_profile_form_save(self):
        """Test profile form save method."""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'Name',
            'email': 'updated@example.com',
            'bio': 'Updated bio',
            'location': 'Updated Location'
        }
        form = UserProfileForm(data=form_data, instance=self.user)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.first_name, 'Updated')
        self.assertEqual(user.email, 'updated@example.com')
        self.assertEqual(user.profile.bio, 'Updated bio')
        self.assertEqual(user.profile.location, 'Updated Location')


@pytest.mark.django_db
class TestAccountsViews:
    """Pytest-style tests for accounts views."""
    
    def test_login_view_status_code(self, client):
        """Test login view returns 200 status code."""
        response = client.get(reverse('accounts:login'))
        assert response.status_code == 200
    
    def test_register_view_status_code(self, client):
        """Test register view returns 200 status code."""
        response = client.get(reverse('accounts:register'))
        assert response.status_code == 200
    
    def test_profile_view_requires_login(self, client):
        """Test profile view requires authentication."""
        response = client.get(reverse('accounts:profile'))
        assert response.status_code == 302
    
    def test_profile_view_authenticated(self, authenticated_client):
        """Test profile view for authenticated user."""
        response = authenticated_client.get(reverse('accounts:profile'))
        assert response.status_code == 200
    
    def test_dashboard_view_authenticated(self, authenticated_client):
        """Test dashboard view for authenticated user."""
        response = authenticated_client.get(reverse('accounts:dashboard'))
        assert response.status_code == 200
    
    def test_user_registration(self, client):
        """Test user registration process."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'New',
            'last_name': 'User',
            'password1': 'newuserpass123',
            'password2': 'newuserpass123'
        }
        response = client.post(reverse('accounts:register'), data)
        assert response.status_code == 302
        assert User.objects.filter(username='newuser').exists()
    
    def test_user_login(self, client, user):
        """Test user login process."""
        data = {
            'username': user.username,
            'password': 'testpass123'
        }
        response = client.post(reverse('accounts:login'), data)
        assert response.status_code == 302


@pytest.mark.django_db
class TestAccountsModels:
    """Pytest-style tests for accounts models."""
    
    def test_user_profile_creation(self, user):
        """Test user profile is created automatically."""
        assert hasattr(user, 'profile')
        assert isinstance(user.profile, UserProfile)
    
    def test_user_profile_str(self, user):
        """Test user profile string representation."""
        expected_str = f"{user.get_full_name()} Profile"
        assert str(user.profile) == expected_str
    
    def test_user_profile_get_absolute_url(self, user):
        """Test user profile get_absolute_url method."""
        expected_url = reverse('accounts:profile')
        assert user.profile.get_absolute_url() == expected_url