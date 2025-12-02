from django.db import models
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.contrib.auth.models import User
from django.utils.text import slugify
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager
from PIL import Image


class BookCategory(models.Model):
    """Book category model."""
    name = models.CharField(_('Name'), max_length=100, unique=True)
    slug = models.SlugField(_('Slug'), unique=True)
    description = models.TextField(_('Description'), blank=True)
    color = models.CharField(_('Color'), max_length=7, default='#3B82F6', help_text=_('Hex color code'))
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)

    class Meta:
        verbose_name = _('Book Category')
        verbose_name_plural = _('Book Categories')
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('books:category_books', kwargs={'slug': self.slug})

    def get_book_count(self):
        """Return number of published books in this category."""
        return self.books.filter(is_published=True).count()


class Book(models.Model):
    """Book model."""
    
    STATUS_CHOICES = [
        ('reading', _('Currently Reading')),
        ('completed', _('Completed')),
        ('want_to_read', _('Want to Read')),
        ('abandoned', _('Abandoned')),
    ]
    
    RATING_CHOICES = [
        (1, '⭐'),
        (2, '⭐⭐'),
        (3, '⭐⭐⭐'),
        (4, '⭐⭐⭐⭐'),
        (5, '⭐⭐⭐⭐⭐'),
    ]
    
    title = models.CharField(_('Title'), max_length=200)
    slug = models.SlugField(_('Slug'), unique=True)
    author = models.CharField(_('Author'), max_length=200)
    isbn = models.CharField(_('ISBN'), max_length=20, blank=True, null=True)
    description = models.TextField(_('Description'), blank=True)
    review = MarkdownxField(_('Review'), blank=True)
    cover_image = models.ImageField(_('Cover Image'), upload_to='books/covers/', blank=True, null=True)
    
    # Book details
    pages = models.PositiveIntegerField(_('Pages'), blank=True, null=True)
    publication_date = models.DateField(_('Publication Date'), blank=True, null=True)
    publisher = models.CharField(_('Publisher'), max_length=200, blank=True)
    language = models.CharField(_('Language'), max_length=50, default='Arabic')
    
    # Reading status
    status = models.CharField(_('Status'), max_length=20, choices=STATUS_CHOICES, default='want_to_read')
    rating = models.PositiveIntegerField(_('Rating'), choices=RATING_CHOICES, blank=True, null=True)
    start_date = models.DateField(_('Start Date'), blank=True, null=True)
    finish_date = models.DateField(_('Finish Date'), blank=True, null=True)
    
    # Relationships
    category = models.ForeignKey(BookCategory, on_delete=models.SET_NULL, null=True, blank=True, related_name='books', verbose_name=_('Category'))
    tags = TaggableManager(verbose_name=_('Tags'), blank=True)
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='books', verbose_name=_('Added By'))
    
    # Publishing
    is_published = models.BooleanField(_('Published'), default=True)
    is_featured = models.BooleanField(_('Featured'), default=False)
    
    # Timestamps
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    # SEO
    meta_description = models.CharField(_('Meta Description'), max_length=160, blank=True)
    meta_keywords = models.CharField(_('Meta Keywords'), max_length=255, blank=True)
    
    class Meta:
        verbose_name = _('Book')
        verbose_name_plural = _('Books')
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['is_published']),
            models.Index(fields=['slug']),
            models.Index(fields=['status']),
        ]

    def __str__(self):
        return f"{self.title} - {self.author}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(f"{self.title}-{self.author}")
        
        # Generate meta description from description if not provided
        if not self.meta_description and self.description:
            self.meta_description = self.description[:160]
        
        super().save(*args, **kwargs)
        
        # Resize cover image
        if self.cover_image:
            self.resize_cover_image()
    
    def get_absolute_url(self):
        return reverse('books:book_detail', kwargs={'slug': self.slug})
    
    def resize_cover_image(self):
        """Resize cover image to optimize file size."""
        try:
            img = Image.open(self.cover_image.path)
            
            # Convert to RGB if necessary
            if img.mode in ('RGBA', 'LA', 'P'):
                img = img.convert('RGB')
            
            # Resize if too large
            max_size = (600, 800)  # Good for book covers
            if img.size[0] > max_size[0] or img.size[1] > max_size[1]:
                img.thumbnail(max_size, Image.Resampling.LANCZOS)
                img.save(self.cover_image.path, 'JPEG', quality=85, optimize=True)
        except Exception:
            pass  # Handle image processing errors gracefully
    
    @property
    def reading_progress(self):
        """Calculate reading progress percentage."""
        if self.status == 'completed':
            return 100
        elif self.status == 'reading' and self.start_date:
            # Simple progress based on days since start
            days_reading = (timezone.now().date() - self.start_date).days
            # Assume average reading speed
            if self.pages:
                estimated_days = self.pages / 20  # 20 pages per day
                progress = min(100, (days_reading / estimated_days) * 100)
                return int(progress)
        return 0
    
    @property
    def reading_time_estimate(self):
        """Estimate reading time in hours."""
        if self.pages:
            # Average reading speed: 250 words per minute, ~250 words per page
            minutes = self.pages * 1  # 1 minute per page
            hours = minutes / 60
            return round(hours, 1)
        return None
    
    def get_rating_display(self):
        """Return rating as stars."""
        if self.rating:
            return '⭐' * self.rating
        return _('Not rated')


class BookNote(models.Model):
    """Notes and quotes from books."""
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='notes', verbose_name=_('Book'))
    title = models.CharField(_('Title'), max_length=200, blank=True)
    content = MarkdownxField(_('Content'))
    page_number = models.PositiveIntegerField(_('Page Number'), blank=True, null=True)
    is_quote = models.BooleanField(_('Is Quote'), default=False)
    is_favorite = models.BooleanField(_('Favorite'), default=False)
    created_at = models.DateTimeField(_('Created At'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Updated At'), auto_now=True)
    
    class Meta:
        verbose_name = _('Book Note')
        verbose_name_plural = _('Book Notes')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.book.title} - {self.title or 'Note'}"