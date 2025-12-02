from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.core import mail
from django.utils import timezone
from django.core.files.uploadedfile import SimpleUploadedFile
from django.conf import settings
from datetime import datetime, timedelta
from .models import UserProfile, LoginAttempt, PasswordResetToken
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserProfileForm
import json


class UserProfileModelTest(TestCase):
    """Test UserProfile model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
        self.profile = self.user.userprofile
    
    def test_profile_creation(self):
        """Test that profile is created automatically."""
        self.assertTrue(hasattr(self.user, 'userprofile'))
        self.assertEqual(self.profile.user, self.user)
    
    def test_get_absolute_url(self):
        """Test profile URL generation."""
        expected_url = reverse('accounts:profile_detail', kwargs={'username': self.user.username})
        self.assertEqual(self.profile.get_absolute_url(), expected_url)
    
    def test_get_age(self):
        """Test age calculation."""
        # Test with birth date
        self.profile.birth_date = datetime(1990, 1, 1).date()
        self.profile.save()
        age = self.profile.get_age()
        self.assertIsInstance(age, int)
        self.assertGreater(age, 0)
        
        # Test without birth date
        self.profile.birth_date = None
        self.profile.save()
        self.assertIsNone(self.profile.get_age())
    
    def test_get_profile_completion(self):
        """Test profile completion calculation."""
        # Empty profile should have low completion
        initial_completion = self.profile.get_completion_percentage()
        self.assertGreater(initial_completion, 0)  # Should have some completion from user fields
        
        # Fill profile fields
        self.profile.bio = 'Test bio'
        self.profile.birth_date = datetime(1990, 1, 1).date()
        self.profile.phone = '+1234567890'
        self.profile.website = 'https://example.com'
        self.profile.country = 'Test Country'
        self.profile.city = 'Test City'
        self.profile.save()
        
        completion = self.profile.get_completion_percentage()
        self.assertGreater(completion, initial_completion)
    
    def test_get_social_links(self):
        """Test social links generation."""
        self.profile.twitter = 'testuser'
        self.profile.linkedin = 'https://linkedin.com/in/testuser'
        self.profile.github = 'testuser'
        self.profile.save()
        
        links = self.profile.get_social_links()
        
        self.assertIn('twitter', links)
        self.assertIn('linkedin', links)
        self.assertIn('github', links)
        
        self.assertEqual(links['twitter'], 'https://twitter.com/testuser')
        self.assertEqual(links['linkedin'], 'https://linkedin.com/in/testuser')
        self.assertEqual(links['github'], 'https://github.com/testuser')
    
    def test_string_representation(self):
        """Test string representation."""
        expected = f"Profile of {self.user.username}"
        self.assertEqual(str(self.profile), expected)


class LoginAttemptModelTest(TestCase):
    """Test LoginAttempt model."""
    
    def test_login_attempt_creation(self):
        """Test login attempt creation."""
        attempt = LoginAttempt.objects.create(
            username='testuser',
            ip_address='127.0.0.1',
            user_agent='Test User Agent',
            success=True
        )
        
        self.assertEqual(attempt.username, 'testuser')
        self.assertEqual(attempt.ip_address, '127.0.0.1')
        self.assertTrue(attempt.success)
        self.assertIsNotNone(attempt.timestamp)
    
    def test_string_representation(self):
        """Test string representation."""
        attempt = LoginAttempt.objects.create(
            username='testuser',
            ip_address='127.0.0.1',
            success=True
        )
        
        expected = f"testuser from 127.0.0.1 - Success"
        self.assertEqual(str(attempt), expected)


class PasswordResetTokenModelTest(TestCase):
    """Test PasswordResetToken model."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
    
    def test_token_creation(self):
        """Test token creation."""
        token = PasswordResetToken.objects.create(user=self.user)
        
        self.assertEqual(token.user, self.user)
        self.assertIsNotNone(token.token)
        self.assertFalse(token.used)
        self.assertIsNone(token.used_at)
        self.assertIsNotNone(token.expires_at)
    
    def test_is_expired(self):
        """Test token expiration."""
        # Create expired token
        token = PasswordResetToken.objects.create(user=self.user)
        token.expires_at = timezone.now() - timedelta(hours=1)
        token.save()
        
        self.assertTrue(token.is_expired())
        
        # Create valid token
        valid_token = PasswordResetToken.objects.create(user=self.user)
        self.assertFalse(valid_token.is_expired())
    
    def test_string_representation(self):
        """Test string representation."""
        token = PasswordResetToken.objects.create(user=self.user)
        expected = f"Password reset token for {self.user.username}"
        self.assertEqual(str(token), expected)


class CustomUserCreationFormTest(TestCase):
    """Test CustomUserCreationForm."""
    
    def test_valid_form(self):
        """Test form with valid data."""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'terms_accepted': True,
            'honeypot': '',
        }
        
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_honeypot_validation(self):
        """Test honeypot spam protection."""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'terms_accepted': True,
            'honeypot': 'spam',  # Honeypot filled
        }
        
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('honeypot', form.errors)
    
    def test_email_uniqueness(self):
        """Test email uniqueness validation."""
        # Create existing user
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='testpass123'
        )
        
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'existing@example.com',  # Duplicate email
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'terms_accepted': True,
            'honeypot': '',
        }
        
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_reserved_username(self):
        """Test reserved username validation."""
        form_data = {
            'username': 'admin',  # Reserved username
            'first_name': 'Admin',
            'last_name': 'User',
            'email': 'admin@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'terms_accepted': True,
            'honeypot': '',
        }
        
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('username', form.errors)
    
    def test_form_save(self):
        """Test form save creates user and profile."""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'terms_accepted': True,
            'honeypot': '',
        }
        
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.first_name, 'New')
        self.assertEqual(user.last_name, 'User')
        
        # Check profile was created
        self.assertTrue(hasattr(user, 'userprofile'))


class UserProfileFormTest(TestCase):
    """Test UserProfileForm."""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123'
        )
        self.profile = self.user.userprofile
    
    def test_valid_form(self):
        """Test form with valid data."""
        form_data = {
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com',
            'bio': 'Updated bio',
            'phone': '+1234567890',
            'website': 'https://example.com',
            'country': 'Test Country',
            'city': 'Test City',
            'language': 'en',
            'timezone': 'UTC',
            'show_email': True,
            'show_phone': False,
            'email_notifications': True,
            'newsletter_subscription': False,
        }
        
        form = UserProfileForm(data=form_data, instance=self.profile)
        self.assertTrue(form.is_valid())
    
    def test_avatar_validation(self):
        """Test avatar file validation."""
        # Test with oversized file
        large_file = SimpleUploadedFile(
            "large.jpg",
            b"x" * (6 * 1024 * 1024),  # 6MB file
            content_type="image/jpeg"
        )
        
        form_data = {
            'first_name': 'Test',
            'last_name': 'User',
            'email': 'test@example.com',
        }
        
        form = UserProfileForm(
            data=form_data,
            files={'avatar': large_file},
            instance=self.profile
        )
        
        self.assertFalse(form.is_valid())
        self.assertIn('avatar', form.errors)


class AccountsViewsTest(TestCase):
    """Test accounts views."""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='Test',
            last_name='User'
        )
    
    def test_register_view_get(self):
        """Test register view GET request."""
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Create Account')
    
    def test_register_view_post_valid(self):
        """Test register view with valid data."""
        form_data = {
            'username': 'newuser',
            'first_name': 'New',
            'last_name': 'User',
            'email': 'newuser@example.com',
            'password1': 'complexpass123',
            'password2': 'complexpass123',
            'terms_accepted': True,
            'honeypot': '',
        }
        
        response = self.client.post(reverse('accounts:register'), data=form_data)
        
        # Should redirect after successful registration
        self.assertEqual(response.status_code, 302)
        
        # Check user was created
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_login_view_get(self):
        """Test login view GET request."""
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Sign In')
    
    def test_login_view_post_valid(self):
        """Test login view with valid credentials."""
        form_data = {
            'username': 'testuser',
            'password': 'testpass123',
        }
        
        response = self.client.post(reverse('accounts:login'), data=form_data)
        
        # Should redirect after successful login
        self.assertEqual(response.status_code, 302)
        
        # Check login attempt was logged
        self.assertTrue(LoginAttempt.objects.filter(username='testuser', success=True).exists())
    
    def test_login_view_post_invalid(self):
        """Test login view with invalid credentials."""
        form_data = {
            'username': 'testuser',
            'password': 'wrongpassword',
        }
        
        response = self.client.post(reverse('accounts:login'), data=form_data)
        
        # Should stay on login page
        self.assertEqual(response.status_code, 200)
        
        # Check failed login attempt was logged
        self.assertTrue(LoginAttempt.objects.filter(username='testuser', success=False).exists())
    
    def test_profile_view_authenticated(self):
        """Test profile view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
    
    def test_profile_view_unauthenticated(self):
        """Test profile view for unauthenticated user."""
        response = self.client.get(reverse('accounts:profile'))
        
        # Should redirect to login
        self.assertEqual(response.status_code, 302)
    
    def test_profile_detail_view(self):
        """Test profile detail view for specific user."""
        response = self.client.get(
            reverse('accounts:profile_detail', kwargs={'username': 'testuser'})
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')
    
    def test_profile_edit_view_authenticated(self):
        """Test profile edit view for authenticated user."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:profile_edit'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Update Profile')
    
    def test_ajax_check_username(self):
        """Test AJAX username availability check."""
        # Test available username
        response = self.client.get(
            reverse('accounts:ajax_check_username'),
            {'username': 'availableuser'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['available'])
        
        # Test taken username
        response = self.client.get(
            reverse('accounts:ajax_check_username'),
            {'username': 'testuser'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['available'])
    
    def test_ajax_check_email(self):
        """Test AJAX email availability check."""
        # Test available email
        response = self.client.get(
            reverse('accounts:ajax_check_email'),
            {'email': 'available@example.com'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertTrue(data['available'])
        
        # Test taken email
        response = self.client.get(
            reverse('accounts:ajax_check_email'),
            {'email': 'test@example.com'}
        )
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertFalse(data['available'])
    
    def test_logout_view(self):
        """Test logout view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.post(reverse('accounts:logout'))
        
        # Should redirect after logout
        self.assertEqual(response.status_code, 302)
    
    def test_dashboard_view(self):
        """Test dashboard view."""
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('accounts:dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Dashboard')


class AccountsSignalsTest(TestCase):
    """Test accounts signals."""
    
    def test_profile_creation_signal(self):
        """Test that profile is created when user is created."""
        user = User.objects.create_user(
            username='signaluser',
            email='signal@example.com',
            password='testpass123'
        )
        
        # Profile should be created automatically
        self.assertTrue(hasattr(user, 'userprofile'))
        self.assertEqual(user.userprofile.user, user)
    
    def test_welcome_email_signal(self):
        """Test that welcome email is sent when user is created."""
        # Clear any existing emails
        mail.outbox = []
        
        User.objects.create_user(
            username='emailuser',
            email='email@example.com',
            password='testpass123'
        )
        
        # Check that welcome email was sent
        self.assertEqual(len(mail.outbox), 1)
        self.assertIn('Welcome', mail.outbox[0].subject)
        self.assertEqual(mail.outbox[0].to, ['email@example.com'])