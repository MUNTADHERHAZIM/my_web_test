from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from markdownx.admin import MarkdownxModelAdmin
from .models import Post, Category, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_post_count', 'color_display', 'created_at']
    list_filter = ['created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['name']
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('name', 'slug', 'description')
        }),
        (_('Display'), {
            'fields': ('color',)
        }),
    )
    
    def get_post_count(self, obj):
        """Display number of posts in category."""
        count = obj.get_post_count()
        if count > 0:
            url = reverse('admin:blog_post_changelist') + f'?category__id__exact={obj.id}'
            return format_html('<a href="{}">{} posts</a>', url, count)
        return '0 posts'
    
    get_post_count.short_description = _('Posts')
    get_post_count.allow_tags = True
    
    def color_display(self, obj):
        """Display color as a colored box."""
        return format_html(
            '<div style="width: 20px; height: 20px; background-color: {}; border: 1px solid #ccc; border-radius: 3px;"></div>',
            obj.color
        )
    
    color_display.short_description = _('Color')
    color_display.allow_tags = True


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'author', 'category', 'is_published', 'is_featured',
        'published_at', 'views_count', 'reading_time', 'get_tags'
    ]
    list_filter = [
        'is_published', 'is_featured', 'category', 'created_at',
        'published_at', 'author'
    ]
    search_fields = ['title', 'excerpt', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'is_featured']
    ordering = ['-created_at']
    date_hierarchy = 'published_at'
    
    fieldsets = (
        (_('Basic Information'), {
            'fields': ('title', 'slug', 'excerpt', 'content')
        }),
        (_('Media'), {
            'fields': ('cover_image',)
        }),
        (_('Classification'), {
            'fields': ('category', 'tags')
        }),
        (_('Publishing'), {
            'fields': ('author', 'is_published', 'is_featured', 'published_at')
        }),
        (_('SEO'), {
            'fields': ('meta_description', 'meta_keywords'),
            'classes': ('collapse',)
        }),
        (_('Statistics'), {
            'fields': ('reading_time', 'views_count'),
            'classes': ('collapse',)
        }),
    )
    
    readonly_fields = ['reading_time', 'views_count']
    
    def get_tags(self, obj):
        """Display tags as comma-separated list."""
        return ', '.join([tag.name for tag in obj.tags.all()])
    
    get_tags.short_description = _('Tags')
    
    def save_model(self, request, obj, form, change):
        """Set author to current user if not set."""
        if not obj.author_id:
            obj.author = request.user
        
        # Set published_at if publishing for the first time
        if obj.is_published and not obj.published_at:
            obj.published_at = timezone.now()
        
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        """Optimize queryset with select_related."""
        return super().get_queryset(request).select_related('author', 'category').prefetch_related('tags')
    
    actions = ['make_published', 'make_unpublished', 'make_featured', 'make_unfeatured']
    
    def make_published(self, request, queryset):
        """Mark selected posts as published."""
        updated = 0
        for post in queryset:
            if not post.is_published:
                post.is_published = True
                if not post.published_at:
                    post.published_at = timezone.now()
                post.save()
                updated += 1
        
        self.message_user(
            request,
            _(f'{updated} posts were successfully marked as published.')
        )
    
    make_published.short_description = _('Mark selected posts as published')
    
    def make_unpublished(self, request, queryset):
        """Mark selected posts as unpublished."""
        updated = queryset.update(is_published=False)
        self.message_user(
            request,
            _(f'{updated} posts were successfully marked as unpublished.')
        )
    
    make_unpublished.short_description = _('Mark selected posts as unpublished')
    
    def make_featured(self, request, queryset):
        """Mark selected posts as featured."""
        updated = queryset.update(is_featured=True)
        self.message_user(
            request,
            _(f'{updated} posts were successfully marked as featured.')
        )
    
    make_featured.short_description = _('Mark selected posts as featured')
    
    def make_unfeatured(self, request, queryset):
        """Mark selected posts as unfeatured."""
        updated = queryset.update(is_featured=False)
        self.message_user(
            request,
            _(f'{updated} posts were successfully marked as unfeatured.')
        )
    
    make_unfeatured.short_description = _('Mark selected posts as unfeatured')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'post', 'is_approved', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['name', 'email', 'content', 'post__title']
    list_editable = ['is_approved']
    ordering = ['-created_at']
    
    fieldsets = (
        (_('Comment Information'), {
            'fields': ('post', 'name', 'email', 'website')
        }),
        (_('Content'), {
            'fields': ('content',)
        }),
        (_('Moderation'), {
            'fields': ('is_approved',)
        }),
    )
    
    readonly_fields = ['post', 'name', 'email', 'website', 'content', 'created_at']
    
    def has_add_permission(self, request):
        """Disable adding comments from admin."""
        return False
    
    actions = ['approve_comments', 'unapprove_comments']
    
    def approve_comments(self, request, queryset):
        """Approve selected comments."""
        updated = queryset.update(is_approved=True)
        self.message_user(
            request,
            _(f'{updated} comments were successfully approved.')
        )
    
    approve_comments.short_description = _('Approve selected comments')
    
    def unapprove_comments(self, request, queryset):
        """Unapprove selected comments."""
        updated = queryset.update(is_approved=False)
        self.message_user(
            request,
            _(f'{updated} comments were successfully unapproved.')
        )
    
    unapprove_comments.short_description = _('Unapprove selected comments')