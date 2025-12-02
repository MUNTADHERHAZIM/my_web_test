from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import UserProfile
import os


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Create UserProfile when a new User is created."""
    if created:
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Save UserProfile when User is saved."""
    try:
        instance.userprofile.save()
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        UserProfile.objects.create(user=instance)


@receiver(post_save, sender=User)
def send_welcome_email(sender, instance, created, **kwargs):
    """Send welcome email to new users."""
    if created and instance.email:
        try:
            # Prepare email context
            context = {
                'user': instance,
                'site_name': getattr(settings, 'SITE_NAME', 'My Website'),
                'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
            }
            
            # Render email templates
            subject = _('Welcome to {}').format(context['site_name'])
            html_message = render_to_string('accounts/emails/welcome_email.html', context)
            plain_message = strip_tags(html_message)
            
            # Send email
            send_mail(
                subject=subject,
                message=plain_message,
                from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                recipient_list=[instance.email],
                html_message=html_message,
                fail_silently=True,  # Don't raise exceptions if email fails
            )
        except Exception as e:
            # Log the error but don't prevent user creation
            print(f"Failed to send welcome email to {instance.email}: {e}")


@receiver(post_delete, sender=UserProfile)
def delete_user_avatar(sender, instance, **kwargs):
    """Delete avatar file when UserProfile is deleted."""
    if instance.avatar:
        try:
            if os.path.isfile(instance.avatar.path):
                os.remove(instance.avatar.path)
        except Exception as e:
            print(f"Failed to delete avatar file: {e}")


@receiver(post_save, sender=UserProfile)
def delete_old_avatar(sender, instance, **kwargs):
    """Delete old avatar when a new one is uploaded."""
    if not instance.pk:
        return
    
    try:
        old_instance = UserProfile.objects.get(pk=instance.pk)
        if old_instance.avatar and old_instance.avatar != instance.avatar:
            if os.path.isfile(old_instance.avatar.path):
                os.remove(old_instance.avatar.path)
    except UserProfile.DoesNotExist:
        pass
    except Exception as e:
        print(f"Failed to delete old avatar file: {e}")


@receiver(post_save, sender=UserProfile)
def update_user_language_preference(sender, instance, **kwargs):
    """Update session language when user changes language preference."""
    # This would be handled in the view when the user is logged in
    # Here we just ensure the preference is saved
    pass


@receiver(post_save, sender=User)
def log_user_registration(sender, instance, created, **kwargs):
    """Log user registration for analytics."""
    if created:
        try:
            # You can integrate with analytics services here
            # For now, just print to console
            print(f"New user registered: {instance.username} ({instance.email})")
            
            # You could also save to a separate analytics model
            # or send to external services like Google Analytics, Mixpanel, etc.
            
        except Exception as e:
            print(f"Failed to log user registration: {e}")


@receiver(post_save, sender=UserProfile)
def notify_admin_profile_completion(sender, instance, **kwargs):
    """Notify admin when user completes profile."""
    completion = instance.get_completion_percentage()
    
    # Notify admin when profile is 100% complete
    if completion == 100:
        try:
            admin_emails = [email for name, email in getattr(settings, 'ADMINS', [])]
            
            if admin_emails:
                context = {
                    'user': instance.user,
                    'profile': instance,
                    'site_name': getattr(settings, 'SITE_NAME', 'My Website'),
                }
                
                subject = _('User Profile Completed: {}').format(instance.user.username)
                html_message = render_to_string('accounts/emails/profile_completed_admin.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                    recipient_list=admin_emails,
                    html_message=html_message,
                    fail_silently=True,
                )
        except Exception as e:
            print(f"Failed to notify admin about profile completion: {e}")


@receiver(post_save, sender=UserProfile)
def send_profile_completion_milestone_email(sender, instance, **kwargs):
    """Send email when user reaches profile completion milestones."""
    completion = instance.get_completion_percentage()
    
    # Send email at 50% and 80% completion
    milestones = [50, 80]
    
    for milestone in milestones:
        if completion >= milestone and instance.user.email:
            # Check if we've already sent this milestone email
            # You might want to track this in a separate model
            try:
                context = {
                    'user': instance.user,
                    'profile': instance,
                    'completion': completion,
                    'milestone': milestone,
                    'site_name': getattr(settings, 'SITE_NAME', 'My Website'),
                    'site_url': getattr(settings, 'SITE_URL', 'http://localhost:8000'),
                }
                
                subject = _('Profile {}% Complete!').format(milestone)
                html_message = render_to_string('accounts/emails/profile_milestone.html', context)
                plain_message = strip_tags(html_message)
                
                send_mail(
                    subject=subject,
                    message=plain_message,
                    from_email=getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@example.com'),
                    recipient_list=[instance.user.email],
                    html_message=html_message,
                    fail_silently=True,
                )
            except Exception as e:
                print(f"Failed to send milestone email: {e}")
            
            # Break after sending the first applicable milestone
            break