from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.html import format_html
from django.urls import reverse
from django.utils.safestring import mark_safe
from .models import UserProfile, LoginAttempt, PasswordResetToken


class UserProfileInline(admin.StackedInline):
    """Inline admin for UserProfile."""
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Profile')
    
    fieldsets = (
        (_('Personal Information'), {
            'fields': ('bio', 'avatar', 'birth_date', 'phone', 'website')
        }),
        (_('Location'), {
            'fields': ('country', 'city')
        }),
        (_('Social Media'), {
            'fields': ('twitter', 'linkedin', 'github')
        }),
        (_('Preferences'), {
            'fields': ('language', 'timezone')
        }),
        (_('Privacy Settings'), {
            'fields': ('show_email', 'show_phone')
        }),
        (_('Notifications'), {
            'fields': ('email_notifications', 'newsletter_subscription')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ('created_at', 'updated_at')


class UserAdmin(BaseUserAdmin):
    """Custom User admin with profile inline."""
    inlines = (UserProfileInline,)
    
    list_display = (
        'username', 'email', 'first_name', 'last_name', 
        'is_staff', 'is_active', 'date_joined', 'profile_completion'
    )
    
    list_filter = (
        'is_staff', 'is_superuser', 'is_active', 'date_joined'
    )
    
    search_fields = ('username', 'first_name', 'last_name', 'email')
    
    def profile_completion(self, obj):
        """Display profile completion percentage."""
        try:
            profile = obj.userprofile
            completion = profile.get_completion_percentage()
            color = 'green' if completion >= 80 else 'orange' if completion >= 50 else 'red'
            return format_html(
                '<span style="color: {}; font-weight: bold;">{}%</span>',
                color, int(completion)
            )
        except UserProfile.DoesNotExist:
            return format_html('<span style="color: red;">No Profile</span>')
    
    profile_completion.short_description = _('Profile Completion')
    profile_completion.admin_order_field = 'userprofile__updated_at'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    """Admin for UserProfile model."""
    
    list_display = (
        'user', 'get_full_name', 'country', 'city', 'language',
        'profile_completion_display', 'email_notifications', 
        'newsletter_subscription', 'created_at'
    )
    
    list_filter = (
        'language', 'country', 'email_notifications', 
        'newsletter_subscription', 'show_email', 'show_phone',
        'created_at', 'updated_at'
    )
    
    search_fields = (
        'user__username', 'user__first_name', 'user__last_name',
        'user__email', 'bio', 'country', 'city'
    )
    
    readonly_fields = (
        'created_at', 'updated_at', 'profile_completion_display',
        'avatar_preview', 'user_link', 'age_display'
    )
    
    fieldsets = (
        (_('User Information'), {
            'fields': ('user_link', 'profile_completion_display')
        }),
        (_('Personal Information'), {
            'fields': ('bio', 'avatar', 'avatar_preview', 'birth_date', 'age_display', 'phone', 'website')
        }),
        (_('Location'), {
            'fields': ('country', 'city')
        }),
        (_('Social Media'), {
            'fields': ('twitter', 'linkedin', 'github'),
            'classes': ('collapse',)
        }),
        (_('Preferences'), {
            'fields': ('language', 'timezone')
        }),
        (_('Privacy Settings'), {
            'fields': ('show_email', 'show_phone')
        }),
        (_('Notifications'), {
            'fields': ('email_notifications', 'newsletter_subscription')
        }),
        (_('Timestamps'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['enable_notifications', 'disable_notifications', 'subscribe_newsletter', 'unsubscribe_newsletter']
    
    def get_full_name(self, obj):
        """Get user's full name."""
        return obj.user.get_full_name() or obj.user.username
    get_full_name.short_description = _('Full Name')
    get_full_name.admin_order_field = 'user__first_name'
    
    def profile_completion_display(self, obj):
        """Display profile completion with progress bar."""
        completion = obj.get_completion_percentage()
        color = '#10b981' if completion >= 80 else '#f59e0b' if completion >= 50 else '#ef4444'
        
        return format_html(
            '<div style="width: 100px; background-color: #e5e7eb; border-radius: 4px; overflow: hidden;">' +
            '<div style="width: {}%; height: 20px; background-color: {}; text-align: center; line-height: 20px; color: white; font-size: 12px; font-weight: bold;">' +
            '{}%</div></div>',
            int(completion), color, int(completion)
        )
    profile_completion_display.short_description = _('Profile Completion')
    
    def avatar_preview(self, obj):
        """Display avatar preview."""
        if obj.avatar:
            return format_html(
                '<img src="{}" style="width: 50px; height: 50px; border-radius: 50%; object-fit: cover;" />',
                obj.avatar.url
            )
        return _('No avatar')
    avatar_preview.short_description = _('Avatar Preview')
    
    def user_link(self, obj):
        """Link to user admin page."""
        url = reverse('admin:auth_user_change', args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', url, obj.user.username)
    user_link.short_description = _('User')
    
    def age_display(self, obj):
        """Display user's age."""
        age = obj.get_age()
        return f"{age} {_('years old')}" if age else _('Not specified')
    age_display.short_description = _('Age')
    
    # Actions
    def enable_notifications(self, request, queryset):
        """Enable email notifications for selected profiles."""
        updated = queryset.update(email_notifications=True)
        self.message_user(request, _(f'{updated} profiles updated to receive email notifications.'))
    enable_notifications.short_description = _('Enable email notifications')
    
    def disable_notifications(self, request, queryset):
        """Disable email notifications for selected profiles."""
        updated = queryset.update(email_notifications=False)
        self.message_user(request, _(f'{updated} profiles updated to not receive email notifications.'))
    disable_notifications.short_description = _('Disable email notifications')
    
    def subscribe_newsletter(self, request, queryset):
        """Subscribe selected profiles to newsletter."""
        updated = queryset.update(newsletter_subscription=True)
        self.message_user(request, _(f'{updated} profiles subscribed to newsletter.'))
    subscribe_newsletter.short_description = _('Subscribe to newsletter')
    
    def unsubscribe_newsletter(self, request, queryset):
        """Unsubscribe selected profiles from newsletter."""
        updated = queryset.update(newsletter_subscription=False)
        self.message_user(request, _(f'{updated} profiles unsubscribed from newsletter.'))
    unsubscribe_newsletter.short_description = _('Unsubscribe from newsletter')


@admin.register(LoginAttempt)
class LoginAttemptAdmin(admin.ModelAdmin):
    """Admin for LoginAttempt model."""
    
    list_display = (
        'username', 'ip_address', 'success', 'timestamp',
        'user_agent_short', 'location_info'
    )
    
    list_filter = (
        'success', 'timestamp', 'ip_address'
    )
    
    search_fields = (
        'username', 'ip_address', 'user_agent'
    )
    
    readonly_fields = (
        'username', 'ip_address', 'user_agent', 'success', 'timestamp'
    )
    
    date_hierarchy = 'timestamp'
    
    ordering = ('-timestamp',)
    
    def has_add_permission(self, request):
        """Disable adding login attempts manually."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable changing login attempts."""
        return False
    
    def user_agent_short(self, obj):
        """Display shortened user agent."""
        if obj.user_agent:
            return obj.user_agent[:50] + '...' if len(obj.user_agent) > 50 else obj.user_agent
        return _('Unknown')
    user_agent_short.short_description = _('User Agent')
    
    def location_info(self, obj):
        """Display location information if available."""
        # This would require a GeoIP service integration
        return _('Location lookup not implemented')
    location_info.short_description = _('Location')
    
    actions = ['delete_selected']
    
    def get_actions(self, request):
        """Customize available actions."""
        actions = super().get_actions(request)
        # Keep only delete action
        return {'delete_selected': actions['delete_selected']}


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    """Admin for PasswordResetToken model."""
    
    list_display = (
        'user', 'token_short', 'created_at', 'expires_at',
        'is_expired', 'used'
    )
    
    list_filter = (
        'used', 'created_at', 'expires_at'
    )
    
    search_fields = (
        'user__username', 'user__email', 'token'
    )
    
    readonly_fields = (
        'user', 'token', 'created_at', 'expires_at', 
        'used', 'is_expired_display'
    )
    
    date_hierarchy = 'created_at'
    
    ordering = ('-created_at',)
    
    def has_add_permission(self, request):
        """Disable adding tokens manually."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable changing tokens."""
        return False
    
    def token_short(self, obj):
        """Display shortened token."""
        return f"{obj.token[:8]}...{obj.token[-8:]}"
    token_short.short_description = _('Token')
    
    def is_expired_display(self, obj):
        """Display expiration status with color."""
        if obj.is_expired():
            return format_html('<span style="color: red; font-weight: bold;">{}</span>', _('Expired'))
        else:
            return format_html('<span style="color: green; font-weight: bold;">{}</span>', _('Valid'))
    is_expired_display.short_description = _('Status')
    
    actions = ['mark_as_used', 'delete_expired']
    
    def mark_as_used(self, request, queryset):
        """Mark selected tokens as used."""
        updated = queryset.filter(used=False).update(used=True)
        self.message_user(request, _(f'{updated} tokens marked as used.'))
    mark_as_used.short_description = _('Mark as used')
    
    def delete_expired(self, request, queryset):
        """Delete expired tokens."""
        from django.utils import timezone
        expired_tokens = queryset.filter(expires_at__lt=timezone.now())
        count = expired_tokens.count()
        expired_tokens.delete()
        self.message_user(request, _(f'{count} expired tokens deleted.'))
    delete_expired.short_description = _('Delete expired tokens')


# Unregister the default User admin and register our custom one
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Customize admin site headers
admin.site.site_header = _('Website Administration')
admin.site.site_title = _('Admin Panel')
admin.site.index_title = _('Welcome to Administration Panel')