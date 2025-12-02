from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from PIL import Image
import os


class UserProfile(models.Model):
    """Extended user profile model."""
    
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        related_name='userprofile',
        verbose_name=_('User')
    )
    
    # Personal Information
    bio = models.TextField(
        max_length=500,
        blank=True,
        verbose_name=_('Bio'),
        help_text=_('Brief description about yourself')
    )
    
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        verbose_name=_('Avatar'),
        help_text=_('Profile picture')
    )
    
    birth_date = models.DateField(
        blank=True,
        null=True,
        verbose_name=_('Birth Date')
    )
    
    phone = models.CharField(
        max_length=20,
        blank=True,
        verbose_name=_('Phone Number')
    )
    
    website = models.URLField(
        blank=True,
        verbose_name=_('Website')
    )
    
    # Location
    country = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Country')
    )
    
    city = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('City')
    )
    
    # Social Media
    twitter = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('Twitter Username'),
        help_text=_('Without @ symbol')
    )
    
    linkedin = models.URLField(
        blank=True,
        verbose_name=_('LinkedIn Profile')
    )
    
    github = models.CharField(
        max_length=100,
        blank=True,
        verbose_name=_('GitHub Username')
    )
    
    # Preferences
    language = models.CharField(
        max_length=10,
        choices=[
            ('en', _('English')),
            ('ar', _('Arabic')),
        ],
        default='en',
        verbose_name=_('Preferred Language')
    )
    
    timezone = models.CharField(
        max_length=50,
        default='UTC',
        verbose_name=_('Timezone')
    )
    
    # Privacy Settings
    show_email = models.BooleanField(
        default=False,
        verbose_name=_('Show Email Publicly')
    )
    
    show_phone = models.BooleanField(
        default=False,
        verbose_name=_('Show Phone Publicly')
    )
    
    # Notifications
    email_notifications = models.BooleanField(
        default=True,
        verbose_name=_('Email Notifications')
    )
    
    newsletter_subscription = models.BooleanField(
        default=False,
        verbose_name=_('Newsletter Subscription')
    )
    
    # Timestamps
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name=_('Updated At')
    )
    
    class Meta:
        verbose_name = _('User Profile')
        verbose_name_plural = _('User Profiles')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.get_full_name() or self.user.username}'s Profile"
    
    def get_absolute_url(self):
        """Return absolute URL for user profile."""
        return reverse('accounts:profile', kwargs={'username': self.user.username})
    
    def get_full_name(self):
        """Return user's full name or username."""
        return self.user.get_full_name() or self.user.username
    
    def get_avatar_url(self):
        """Return avatar URL or default avatar."""
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return '/static/images/default-avatar.svg'
    
    def save(self, *args, **kwargs):
        """Override save to resize avatar image."""
        super().save(*args, **kwargs)
        
        if self.avatar:
            self.resize_avatar()
    
    def resize_avatar(self):
        """Resize avatar image to 300x300 pixels."""
        try:
            img = Image.open(self.avatar.path)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize image
            if img.height > 300 or img.width > 300:
                output_size = (300, 300)
                img.thumbnail(output_size, Image.Resampling.LANCZOS)
                img.save(self.avatar.path, 'JPEG', quality=85, optimize=True)
        except Exception as e:
            # Log error but don't raise exception
            print(f"Error resizing avatar: {e}")
    
    def get_social_links(self):
        """Return dictionary of social media links."""
        links = {}
        
        if self.twitter:
            links['twitter'] = f'https://twitter.com/{self.twitter}'
        
        if self.linkedin:
            links['linkedin'] = self.linkedin
        
        if self.github:
            links['github'] = f'https://github.com/{self.github}'
        
        if self.website:
            links['website'] = self.website
        
        return links
    
    def get_age(self):
        """Calculate and return user's age."""
        if not self.birth_date:
            return None
        
        from datetime import date
        today = date.today()
        return today.year - self.birth_date.year - (
            (today.month, today.day) < (self.birth_date.month, self.birth_date.day)
        )
    
    def is_profile_complete(self):
        """Check if profile is complete."""
        required_fields = [
            self.user.first_name,
            self.user.last_name,
            self.bio,
            self.avatar
        ]
        return all(field for field in required_fields)
    
    def get_completion_percentage(self):
        """Calculate profile completion percentage."""
        fields = [
            self.user.first_name,
            self.user.last_name,
            self.user.email,
            self.bio,
            self.avatar,
            self.birth_date,
            self.phone,
            self.country,
            self.city
        ]
        
        completed_fields = sum(1 for field in fields if field)
        return int((completed_fields / len(fields)) * 100)
    
    @property
    def completion_percentage(self):
        """Property for template access to completion percentage."""
        return self.get_completion_percentage()


class LoginAttempt(models.Model):
    """Track login attempts for security."""
    
    username = models.CharField(
        max_length=150,
        verbose_name=_('Username')
    )
    
    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP Address')
    )
    
    user_agent = models.TextField(
        blank=True,
        verbose_name=_('User Agent')
    )
    
    success = models.BooleanField(
        default=False,
        verbose_name=_('Success')
    )
    
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Timestamp')
    )
    
    class Meta:
        verbose_name = _('Login Attempt')
        verbose_name_plural = _('Login Attempts')
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['username', 'timestamp']),
            models.Index(fields=['ip_address', 'timestamp']),
        ]
    
    def __str__(self):
        status = _('Success') if self.success else _('Failed')
        return f"{self.username} - {status} - {self.timestamp}"


class PasswordResetToken(models.Model):
    """Custom password reset token model."""
    
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='password_reset_tokens',
        verbose_name=_('User')
    )
    
    token = models.CharField(
        max_length=100,
        unique=True,
        verbose_name=_('Token')
    )
    
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Created At')
    )
    
    used = models.BooleanField(
        default=False,
        verbose_name=_('Used')
    )
    
    expires_at = models.DateTimeField(
        verbose_name=_('Expires At')
    )
    
    class Meta:
        verbose_name = _('Password Reset Token')
        verbose_name_plural = _('Password Reset Tokens')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Reset token for {self.user.username}"
    
    def is_expired(self):
        """Check if token is expired."""
        from django.utils import timezone
        return timezone.now() > self.expires_at
    
    def is_valid(self):
        """Check if token is valid (not used and not expired)."""
        return not self.used and not self.is_expired()