from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Project, ContactMessage, SiteSettings
from .forms import ContactForm

User = get_user_model()


class ProjectModelTest(TestCase):
    """Test Project model."""
    
    def setUp(self):
        self.project = Project.objects.create(
            title='Test Project',
            slug='test-project',
            description='Test description',
            short_description='Short test description',
            technologies='Python, Django, JavaScript'
        )
    
    def test_project_creation(self):
        """Test project creation."""
        self.assertEqual(self.project.title, 'Test Project')
        self.assertEqual(self.project.slug, 'test-project')
        self.assertEqual(str(self.project), 'Test Project')
    
    def test_get_technologies_list(self):
        """Test technologies list method."""
        technologies = self.project.get_technologies_list()
        self.assertEqual(technologies, ['Python', 'Django', 'JavaScript'])
    
    def test_get_absolute_url(self):
        """Test get absolute URL."""
        url = self.project.get_absolute_url()
        self.assertEqual(url, reverse('core:project_detail', kwargs={'slug': 'test-project'}))


class ContactMessageModelTest(TestCase):
    """Test ContactMessage model."""
    
    def setUp(self):
        self.message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Test Subject',
            message='Test message content'
        )
    
    def test_contact_message_creation(self):
        """Test contact message creation."""
        self.assertEqual(self.message.name, 'Test User')
        self.assertEqual(self.message.email, 'test@example.com')
        self.assertEqual(str(self.message), 'Test User - Test Subject')
        self.assertFalse(self.message.is_read)


class SiteSettingsModelTest(TestCase):
    """Test SiteSettings model."""
    
    def test_get_settings(self):
        """Test get settings method."""
        settings = SiteSettings.get_settings()
        self.assertIsInstance(settings, SiteSettings)
        self.assertEqual(settings.site_title, 'منتظر حازم ثامر')


class CoreViewsTest(TestCase):
    """Test core views."""
    
    def setUp(self):
        self.client = Client()
        self.project = Project.objects.create(
            title='Test Project',
            slug='test-project',
            description='Test description',
            short_description='Short test description',
            technologies='Python, Django'
        )
    
    def test_home_view(self):
        """Test home page view."""
        response = self.client.get(reverse('core:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'منتظر حازم ثامر')
    
    def test_about_view(self):
        """Test about page view."""
        response = self.client.get(reverse('core:about'))
        self.assertEqual(response.status_code, 200)
    
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
            'message': 'This is a test message with enough content.'
        }
        response = self.client.post(reverse('core:contact'), data)
        self.assertEqual(response.status_code, 302)  # Redirect after success
        self.assertTrue(ContactMessage.objects.filter(email='test@example.com').exists())
    
    def test_projects_view(self):
        """Test projects list view."""
        response = self.client.get(reverse('core:projects'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
    
    def test_project_detail_view(self):
        """Test project detail view."""
        response = self.client.get(reverse('core:project_detail', kwargs={'slug': 'test-project'}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Project')
    
    def test_privacy_policy_view(self):
        """Test privacy policy view."""
        response = self.client.get(reverse('core:privacy_policy'))
        self.assertEqual(response.status_code, 200)
    
    def test_terms_of_service_view(self):
        """Test terms of service view."""
        response = self.client.get(reverse('core:terms_of_service'))
        self.assertEqual(response.status_code, 200)
    
    def test_robots_txt_view(self):
        """Test robots.txt view."""
        response = self.client.get(reverse('core:robots_txt'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response['Content-Type'], 'text/plain')
        self.assertContains(response, 'User-agent: *')


class ContactFormTest(TestCase):
    """Test contact form."""
    
    def test_valid_form(self):
        """Test form with valid data."""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message with enough content.'
        }
        form = ContactForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_honeypot_protection(self):
        """Test honeypot protection."""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message.',
            'website': 'http://spam.com'  # Honeypot field
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('website', form.errors)
    
    def test_short_name_validation(self):
        """Test name validation."""
        form_data = {
            'name': 'A',  # Too short
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'This is a test message with enough content.'
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('name', form.errors)
    
    def test_short_message_validation(self):
        """Test message validation."""
        form_data = {
            'name': 'Test User',
            'email': 'test@example.com',
            'subject': 'Test Subject',
            'message': 'Short'  # Too short
        }
        form = ContactForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('message', form.errors)