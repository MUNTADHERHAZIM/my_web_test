from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from .models import Project, ContactMessage, SiteSettings, Announcement


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_featured', 'order', 'created_at', 'view_links']
    list_filter = ['is_featured', 'created_at']
    search_fields = ['title', 'description', 'technologies']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_featured', 'order']
    ordering = ['order', '-created_at']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        (_('Media'), {
            'fields': ('image',)
        }),
        (_('Technical Details'), {
            'fields': ('technologies',)
        }),
        (_('Links'), {
            'fields': ('github_url', 'live_url')
        }),
        (_('Display Options'), {
            'fields': ('is_featured', 'order')
        }),
    )
    
    def view_links(self, obj):
        """Display view links for the project."""
        links = []
        if obj.github_url:
            links.append(f'<a href="{obj.github_url}" target="_blank" class="button">GitHub</a>')
        if obj.live_url:
            links.append(f'<a href="{obj.live_url}" target="_blank" class="button">Live Demo</a>')
        return format_html(' '.join(links)) if links else '-'
    
    view_links.short_description = _('Links')
    view_links.allow_tags = True


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'subject', 'is_read', 'created_at']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['is_read']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Contact Information'), {
            'fields': ('name', 'email', 'created_at')
        }),
        (_('Message'), {
            'fields': ('subject', 'message')
        }),
        (_('Status'), {
            'fields': ('is_read',)
        }),
    )
    
    def has_add_permission(self, request):
        """Disable adding contact messages from admin."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Allow deleting contact messages."""
        return True


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('Site Information'), {
            'fields': ('site_title', 'site_tagline', 'about_text', 'profile_image')
        }),
        (_('Contact Information'), {
            'fields': ('email', 'phone', 'location')
        }),
        (_('Social Media'), {
            'fields': ('github_url', 'linkedin_url', 'twitter_url')
        }),
        (_('SEO Settings'), {
            'fields': ('meta_description', 'meta_keywords')
        }),
        (_('Analytics'), {
            'fields': ('google_analytics_id',)
        }),
    )
    
    def has_add_permission(self, request):
        """Only allow one instance of site settings."""
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Prevent deletion of site settings."""
        return False


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'announcement_type', 'priority', 'is_active', 
        'show_countdown', 'start_date', 'end_date', 'status_display'
    ]
    list_filter = [
        'announcement_type', 'priority', 'is_active', 'show_countdown',
        'show_on_all_pages', 'is_dismissible', 'start_date', 'end_date'
    ]
    search_fields = ['title', 'message']
    list_editable = ['is_active', 'priority']
    ordering = ['-priority', '-created_at']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'message', 'announcement_type', 'priority')
        }),
        (_('Display Settings'), {
            'fields': ('is_active', 'show_on_all_pages', 'is_dismissible', 'show_countdown')
        }),
        (_('Timing'), {
            'fields': ('start_date', 'end_date'),
            'description': _('Leave end date empty for permanent announcements')
        }),
        (_('Styling'), {
            'fields': ('background_color', 'text_color'),
            'classes': ('collapse',)
        }),
        (_('Optional Link'), {
            'fields': ('link_url', 'link_text'),
            'classes': ('collapse',)
        }),
        (_('Metadata'), {
            'fields': ('created_by',),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['created_at', 'updated_at']
    
    def status_display(self, obj):
        """Display current status of announcement."""
        if obj.is_currently_active():
            return format_html(
                '<span style="color: green; font-weight: bold;">🟢 {}</span>',
                _('Active')
            )
        elif not obj.is_active:
            return format_html(
                '<span style="color: red; font-weight: bold;">🔴 {}</span>',
                _('Inactive')
            )
        elif obj.start_date > timezone.now():
            return format_html(
                '<span style="color: orange; font-weight: bold;">🟡 {}</span>',
                _('Scheduled')
            )
        else:
            return format_html(
                '<span style="color: gray; font-weight: bold;">⚫ {}</span>',
                _('Expired')
            )
    
    status_display.short_description = _('Status')
    
    def save_model(self, request, obj, form, change):
        """Set created_by field when saving."""
        if not change:  # Only set on creation
            obj.created_by = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('created_by')
    
    class Media:
        css = {
            'all': ('admin/css/announcement_admin.css',)
        }
        js = ('admin/js/announcement_admin.js',)


# Customize admin site
admin.site.site_header = _('منتظر حازم ثامر - لوحة الإدارة')
admin.site.site_title = _('إدارة الموقع')
admin.site.index_title = _('مرحباً بك في لوحة إدارة موقعك')