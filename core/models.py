from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.core.validators import URLValidator
from django.utils import timezone


class Project(models.Model):
    """Model for portfolio projects."""
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'))
    short_description = models.CharField(_('Short Description'), max_length=300)
    image = models.ImageField(_('Image'), upload_to='projects/', blank=True, null=True)
    technologies = models.CharField(_('Technologies'), max_length=500, help_text=_('Comma-separated list of technologies'))
    github_url = models.URLField(_('GitHub URL'), blank=True, null=True)
    live_url = models.URLField(_('Live Demo URL'), blank=True, null=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    order = models.PositiveIntegerField(_('Order'), default=0)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:project_detail', kwargs={'slug': self.slug})

    def get_technologies_list(self):
        """Return technologies as a list."""
        return [tech.strip() for tech in self.technologies.split(',') if tech.strip()]


class ContactMessage(models.Model):
    """Model for contact form messages."""
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    subject = models.CharField(_('Subject'), max_length=200)
    message = models.TextField(_('Message'))
    is_read = models.BooleanField(_('Read'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Contact Message')
        verbose_name_plural = _('Contact Messages')
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} - {self.subject}'


class SiteSettings(models.Model):
    """Model for site-wide settings."""
    site_title = models.CharField(_('Site Title'), max_length=100, default='منتظر حازم ثامر')
    site_tagline = models.CharField(_('Site Tagline'), max_length=200, default='مطور برمجيات – Django & Web')
    about_text = models.TextField(_('About Text'), default='مطور ويب شغوف ببناء تطبيقات نظيفة وقابلة للتوسع.')
    profile_image = models.ImageField(_('Profile Image'), upload_to='profile/', blank=True, null=True)
    
    # Contact Information
    email = models.EmailField(_('Email'), default='contact@yourdomain.com')
    phone = models.CharField(_('Phone'), max_length=20, blank=True)
    location = models.CharField(_('Location'), max_length=100, blank=True)
    
    # Social Media Links
    github_url = models.URLField(_('GitHub URL'), blank=True)
    linkedin_url = models.URLField(_('LinkedIn URL'), blank=True)
    twitter_url = models.URLField(_('Twitter/X URL'), blank=True)
    
    # SEO Settings
    meta_description = models.TextField(_('Meta Description'), max_length=160, blank=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=255, blank=True)
    
    # Analytics
    google_analytics_id = models.CharField(_('Google Analytics ID'), max_length=20, blank=True)
    
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)

    class Meta:
        verbose_name = _('Site Settings')
        verbose_name_plural = _('Site Settings')

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        # Ensure only one instance exists
        if not self.pk and SiteSettings.objects.exists():
            raise ValueError('Only one SiteSettings instance is allowed')
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        """Get or create site settings."""
        settings, created = cls.objects.get_or_create(pk=1)
        return settings


class Announcement(models.Model):
    """Model for site-wide announcements."""
    ANNOUNCEMENT_TYPES = [
        ('info', _('Information')),
        ('success', _('Success')),
        ('warning', _('Warning')),
        ('error', _('Error')),
        ('celebration', _('Celebration')),
        ('holiday', _('Holiday')),
        ('mourning', _('Mourning')),
        ('event', _('Event')),
    ]
    
    PRIORITY_CHOICES = [
        ('low', _('Low')),
        ('medium', _('Medium')),
        ('high', _('High')),
        ('urgent', _('Urgent')),
    ]
    
    title = models.CharField(_('Title'), max_length=200)
    message = models.TextField(_('Message'))
    announcement_type = models.CharField(
        _('Type'), 
        max_length=20, 
        choices=ANNOUNCEMENT_TYPES, 
        default='info'
    )
    priority = models.CharField(
        _('Priority'), 
        max_length=10, 
        choices=PRIORITY_CHOICES, 
        default='medium'
    )
    
    # Display settings
    is_active = models.BooleanField(_('Active'), default=True)
    show_countdown = models.BooleanField(_('Show Countdown'), default=False)
    is_dismissible = models.BooleanField(_('Dismissible'), default=True)
    show_on_all_pages = models.BooleanField(_('Show on All Pages'), default=True)
    
    # Timing
    start_date = models.DateTimeField(_('Start Date'), default=timezone.now)
    end_date = models.DateTimeField(_('End Date'), blank=True, null=True)
    
    # Styling
    background_color = models.CharField(
        _('Background Color'), 
        max_length=7, 
        default='#3B82F6',
        help_text=_('Hex color code (e.g., #3B82F6)')
    )
    text_color = models.CharField(
        _('Text Color'), 
        max_length=7, 
        default='#FFFFFF',
        help_text=_('Hex color code (e.g., #FFFFFF)')
    )
    
    # Optional link
    link_url = models.URLField(_('Link URL'), blank=True, null=True)
    link_text = models.CharField(_('Link Text'), max_length=100, blank=True)
    
    # Metadata
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    created_by = models.ForeignKey(
        'auth.User', 
        on_delete=models.CASCADE, 
        verbose_name=_('Created By'),
        blank=True,
        null=True
    )
    
    class Meta:
        verbose_name = _('Announcement')
        verbose_name_plural = _('Announcements')
        ordering = ['-priority', '-created_at']
    
    def __str__(self):
        return self.title
    
    def is_currently_active(self):
        """Check if announcement is currently active."""
        now = timezone.now()
        if not self.is_active:
            return False
        if self.start_date > now:
            return False
        if self.end_date and self.end_date < now:
            return False
        return True
    
    def get_type_icon(self):
        """Get icon for announcement type."""
        icons = {
            'info': 'fas fa-info-circle',
            'success': 'fas fa-check-circle',
            'warning': 'fas fa-exclamation-triangle',
            'error': 'fas fa-times-circle',
            'celebration': 'fas fa-party-horn',
            'holiday': 'fas fa-calendar-star',
            'mourning': 'fas fa-heart',
            'event': 'fas fa-calendar-alt',
        }
        return icons.get(self.announcement_type, 'fas fa-info-circle')
    
    def get_priority_class(self):
        """Get CSS class for priority."""
        classes = {
            'low': 'priority-low',
            'medium': 'priority-medium',
            'high': 'priority-high',
            'urgent': 'priority-urgent',
        }
        return classes.get(self.priority, 'priority-medium')
    
    def time_remaining(self):
        """Get time remaining until end date."""
        if not self.end_date:
            return None
        now = timezone.now()
        if self.end_date <= now:
            return None
        return self.end_date - now