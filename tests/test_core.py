"""Tests for the core application."""

import pytest
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils.translation import activate

from core.models import Project, ContactMessage
from core.forms import ContactForm

User = get_user_model()


class CoreViewsTestCase(TestCase):
    """Test cases for core views."""
    
    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123"
        )
        
        self.project = Project.objects.create(
            title_en="Test Project",
            title_ar="مشروع تجريبي",
            slug="test-project",
            description_en="Test description",
            description_ar="وصف تجريبي",
            content_en="Test content",
            content_ar="محتوى تجريبي",
            technologies="Django, Python",
            featured=True,
            completed=True
        )
    
    def test_home_view(self):
        """Test home page view."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'منتظر حازم ثامر')
        self.assertContains(response, 'Muntadher Hazim Thamer')
    
    def test_about_view(self):
        """Test about page view."""
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'About')
    
    def test_contact_view_get(self):
        """Test contact page GET request."""
        response = self.client.get(reverse('core:contact'))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], ContactForm)
    
    def test_contact_view_post_valid(self):
        """Test contact page POST request with valid data."""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        response = self.client.post(reverse('core:contact'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ContactMessage.objects.filter(email='test@example.com').exists())
    
    def test_contact_view_post_invalid(self):
        """Test contact page POST request with invalid data."""
        data = {
            'name': '',  # Required field
            'email': 'invalid-email',
            'subject': '',
            'message': ''
        }
        response = self.client.post(reverse('core:contact'), data)
        self.assertEqual(response.status_code, 200)  # Stay on page with errors
        self.assertFormError(response, 'form', 'name', 'This field is required.')
    
    def test_projects_view(self):
        """Test projects page view."""
        response = self.client.get(reverse('core:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.project.title_en)
        self.assertIn(self.project, response.context['projects'])
    
    def test_project_detail_view(self):
        """Test project detail view."""
        response = self.client.get(
            reverse('core:project_detail', kwargs={'slug': self.project.slug})
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['project'], self.project)
    
    def test_project_detail_view_404(self):
        """Test project detail view with non-existent slug."""
        response = self.client.get(
            reverse('core:project_detail', kwargs={'slug': 'non-existent'})
        )
        self.assertEqual(response.status_code, 404)


class ProjectModelTestCase(TestCase):
    """Test cases for Project model."""
    
    def setUp(self):
        """Set up test data."""
        self.project = Project.objects.create(
            title_en="Test Project",
            title_ar="مشروع تجريبي",
            slug="test-project",
            description_en="Test description",
            description_ar="وصف تجريبي",
            content_en="Test content",
            content_ar="محتوى تجريبي",
            technologies="Django, Python, PostgreSQL",
            github_url="https://github.com/test/project",
            live_url="https://testproject.com",
            featured=True,
            completed=True
        )
    
    def test_project_str_representation(self):
        """Test project string representation."""
        activate('en')
        self.assertEqual(str(self.project), "Test Project")
        
        activate('ar')
        self.assertEqual(str(self.project), "مشروع تجريبي")
    
    def test_project_get_absolute_url(self):
        """Test project get_absolute_url method."""
        expected_url = reverse('core:project_detail', kwargs={'slug': self.project.slug})
        self.assertEqual(self.project.get_absolute_url(), expected_url)
    
    def test_project_technologies_list(self):
        """Test project technologies_list property."""
        expected_technologies = ['Django', 'Python', 'PostgreSQL']
        self.assertEqual(self.project.technologies_list, expected_technologies)
    
    def test_project_slug_uniqueness(self):
        """Test project slug uniqueness."""
        with self.assertRaises(Exception):
            Project.objects.create(
                title_en="Another Project",
                title_ar="مشروع آخر",
                slug="test-project",  # Same slug
                description_en="Another description",
                description_ar="وصف آخر",
                content_en="Another content",
                content_ar="محتوى آخر",
                technologies="React, Node.js"
            )


class ContactMessageModelTestCase(TestCase):
    """Test cases for ContactMessage model."""
    
    def setUp(self):
        """Set up test data."""
        self.message = ContactMessage.objects.create(
            name="Test User",
            email="test@example.com",
            subject="Test Subject",
            message="This is a test message.",
            ip_address="127.0.0.1"
        )
    
    def test_contact_message_str_representation(self):
        """Test contact message string representation."""
        expected_str = f"{self.message.subject} - {self.message.name}"
        self.assertEqual(str(self.message), expected_str)
    
    def test_contact_message_creation(self):
        """Test contact message creation."""
        self.assertEqual(self.message.name, "Test User")
        self.assertEqual(self.message.email, "test@example.com")
        self.assertEqual(self.message.subject, "Test Subject")
        self.assertEqual(self.message.message, "This is a test message.")
        self.assertEqual(self.message.ip_address, "127.0.0.1")
        self.assertFalse(self.message.is_read)
        self.assertIsNotNone(self.message.created_at)


class ContactFormTestCase(TestCase):
    """Test cases for ContactForm."""
    
    def test_contact_form_valid_data(self):
        """Test contact form with valid data."""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_contact_form_missing_required_fields(self):
        """Test contact form with missing required fields."""
        form_data = {
            'name': '',
            'email': '',
            'subject': '',
            'message': ''
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('subject', form.errors)
        self.assertIn('message', form.errors)
    
    def test_contact_form_invalid_email(self):
        """Test contact form with invalid email."""
        form_data = {
            'name': 'Test User',
            'email': 'invalid-email',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)
    
    def test_contact_form_save(self):
        """Test contact form save method."""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        message = form.save(ip_address='127.0.0.1')
        self.assertIsInstance(message, ContactMessage)
        self.assertEqual(message.name, 'Test User')
        self.assertEqual(message.email, 'test@example.com')
        self.assertEqual(message.ip_address, '127.0.0.1')


@pytest.mark.django_db
class TestCoreViews:
    """Pytest-style tests for core views."""
    
    def test_home_view_status_code(self, client):
        """Test home view returns 200 status code."""
        response = client.get(reverse('core:home'))
        assert response.status_code == 200
    
    def test_home_view_contains_name(self, client):
        """Test home view contains the developer name."""
        response = client.get(reverse('core:home'))
        assert 'منتظر حازم ثامر' in response.content.decode()
        assert 'Muntadher Hazim Thamer' in response.content.decode()
    
    def test_projects_view_with_project(self, client, project):
        """Test projects view displays project."""
        response = client.get(reverse('core:projects'))
        assert response.status_code == 200
        assert project.title_en in response.content.decode()
    
    def test_contact_form_submission(self, client):
        """Test contact form submission."""
        data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Test message content'
        }
        response = client.post(reverse('core:contact'), data)
        assert response.status_code == 302
        assert ContactMessage.objects.filter(email='test@example.com').exists()