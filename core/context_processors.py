from .models import SiteSettings, Announcement
from django.utils import timezone
from django.db import models


def site_settings(request):
    """Add site settings to template context."""
    try:
        settings = SiteSettings.get_settings()
        return {
            'site_settings': settings,
        }
    except Exception:
        # Return default values if settings don't exist
        return {
            'site_settings': {
                'site_title': 'منتظر حازم ثامر',
                'site_tagline': 'مطور برمجيات – Django & Web',
                'email': 'contact@yourdomain.com',
                'github_url': '',
                'linkedin_url': '',
                'twitter_url': '',
            }
        }


def active_announcements(request):
    """Add active announcements to template context."""
    try:
        now = timezone.now()
        announcements = Announcement.objects.filter(
            is_active=True,
            show_on_all_pages=True,
            start_date__lte=now
        ).filter(
            models.Q(end_date__isnull=True) | models.Q(end_date__gt=now)
        ).order_by('-priority', '-created_at')
        
        return {
            'active_announcements': announcements,
            'has_announcements': announcements.exists(),
        }
    except Exception:
        # Return empty if there's an error
        return {
            'active_announcements': [],
            'has_announcements': False,
        }