import re
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager
from PIL import Image
import math


class Category(models.Model):
    """Blog category model."""
    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'), blank=True)
    color = models.CharField(_('Color'), max_length=7, default='#3B82F6', help_text=_('Hex color code'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category_posts', kwargs={'slug': self.slug})

    def get_post_count(self):
        """Return number of published posts in this category."""
        return self.posts.filter(is_published=True).count()


class PostManager(models.Manager):
    """Custom manager for Post model."""
    
    def published(self):
        """Return only published posts."""
        return self.filter(is_published=True, published_at__lte=timezone.now())
    
    def featured(self):
        """Return featured posts."""
        return self.published().filter(is_featured=True)


class Post(models.Model):
    """Blog post model."""
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    excerpt = models.TextField(_('Excerpt'), max_length=300, help_text=_('Brief description of the post'))
    content = RichTextUploadingField(_('Content'))
    cover_image = models.ImageField(_('Cover Image'), upload_to='blog/covers/', blank=True, null=True)
    
    # Metadata
    reading_time = models.PositiveIntegerField(_('Reading Time (minutes)'), default=1)
    views_count = models.PositiveIntegerField(_('Views Count'), default=0)
    
    # Relationships
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts', verbose_name=_('Author'))
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='posts', verbose_name=_('Category'))
    tags = TaggableManager(verbose_name=_('Tags'), blank=True)
    
    # Publishing
    is_published = models.BooleanField(_('Published'), default=False)
    is_featured = models.BooleanField(_('Featured'), default=False)
    published_at = models.DateTimeField(_('Published At'), blank=True, null=True)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    # SEO
    meta_description = models.CharField(_('Meta Description'), max_length=160, blank=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=255, blank=True)
    
    objects = PostManager()
    
    class Meta:
        verbose_name = _('Post')
        verbose_name_plural = _('Posts')
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['is_published']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set published_at when publishing for the first time
        if self.is_published and not self.published_at:
            self.published_at = timezone.now()
        
        # Calculate reading time
        if self.content:
            self.reading_time = self.calculate_reading_time()
        
        # Generate meta description from excerpt if not provided
        if not self.meta_description and self.excerpt:
            self.meta_description = self.excerpt[:160]
        
        super().save(*args, **kwargs)
        
        # Resize cover image
        if self.cover_image:
            self.resize_cover_image()
    
    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})
    
    def calculate_reading_time(self):
        """Calculate reading time based on content length."""
        # Remove markdown syntax and count words
        text = re.sub(r'[#*`\[\]()_~]', '', self.content)
        word_count = len(text.split())
        # Average reading speed: 200 words per minute
        reading_time = math.ceil(word_count / 200)
        return max(1, reading_time)  # Minimum 1 minute
    
    def resize_cover_image(self):
        """Resize cover image to optimize file size."""
        try:
            img = Image.open(self.cover_image.path)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            max_size = (1200, 630)  # Good for social media sharing
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(self.cover_image.path, 'JPEG', quality=85, optimize=True)
        except Exception:
            pass  # Handle image processing errors gracefully
    
    def get_related_posts(self, count=3):
        """Get related posts based on category and tags."""
        related_posts = Post.objects.published().exclude(id=self.id)
        
        # Filter by category first
        if self.category:
            related_posts = related_posts.filter(category=self.category)
        
        # If not enough posts, include posts with similar tags
        if related_posts.count() < count:
            tag_names = list(self.tags.names())
            if tag_names:
                related_posts = Post.objects.published().exclude(id=self.id).filter(
                    tags__name__in=tag_names
                ).distinct()
        
        return related_posts[:count]
    
    def increment_views(self):
        """Increment views count."""
        self.views_count += 1
        self.save(update_fields=['views_count'])
    
    @property
    def reading_time_display(self):
        """Return reading time with proper Arabic text."""
        if self.reading_time == 1:
            return _('دقيقة واحدة')
        elif self.reading_time == 2:
            return _('دقيقتان')
        elif 3 <= self.reading_time <= 10:
            return _(f'{self.reading_time} دقائق')
        else:
            return _(f'{self.reading_time} دقيقة')


class Comment(models.Model):
    """Comment model for blog posts."""
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name=_('Post'))
    name = models.CharField(_('Name'), max_length=100)
    email = models.EmailField(_('Email'))
    website = models.URLField(_('Website'), blank=True)
    content = models.TextField(_('Comment'))
    is_approved = models.BooleanField(_('Approved'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    
    class Meta:
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')
        ordering = ['-created_at']
    
    def __str__(self):
        return f'{self.name} on {self.post.title}'