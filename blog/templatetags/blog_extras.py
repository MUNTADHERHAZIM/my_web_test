"""Custom template tags for the blog app."""

from django import template
from django.utils.safestring import mark_safe
from django.utils.html import format_html
from django.urls import reverse
from django.utils.translation import gettext as _
import re
import markdown
from markdown.extensions import codehilite, toc

register = template.Library()


@register.filter
def markdown_to_html(text):
    """Convert markdown text to HTML."""
    if not text:
        return ''
    
    md = markdown.Markdown(
        extensions=[
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
            'markdown.extensions.fenced_code',
            'markdown.extensions.tables',
            'markdown.extensions.nl2br',
        ],
        extension_configs={
            'markdown.extensions.codehilite': {
                'css_class': 'highlight',
                'use_pygments': True,
            },
            'markdown.extensions.toc': {
                'permalink': True,
            },
        }
    )
    
    return mark_safe(md.convert(text))


@register.filter
def reading_time(content):
    """Calculate estimated reading time for content."""
    if not content:
        return 0
    
    # Remove HTML tags and count words
    text = re.sub(r'<[^>]+>', '', str(content))
    word_count = len(text.split())
    
    # Average reading speed is 200-250 words per minute
    # We'll use 200 for a conservative estimate
    minutes = max(1, round(word_count / 200))
    return minutes


@register.filter
def truncate_chars_html(value, length):
    """Truncate HTML content while preserving tags."""
    if not value:
        return ''
    
    if len(value) <= length:
        return value
    
    # Simple truncation that tries to avoid breaking HTML
    truncated = value[:length]
    
    # Find the last complete word
    last_space = truncated.rfind(' ')
    if last_space > 0:
        truncated = truncated[:last_space]
    
    return truncated + '...'


@register.simple_tag
def get_related_posts(post, limit=3):
    """Get related posts based on tags and category."""
    if not post:
        return []
    
    from blog.models import Post
    
    # Get posts with same tags or category
    related = Post.objects.published().exclude(id=post.id)
    
    if post.category:
        related = related.filter(category=post.category)
    
    if post.tags.exists():
        tag_ids = post.tags.values_list('id', flat=True)
        related = related.filter(tags__in=tag_ids).distinct()
    
    return related.select_related('author', 'category')[:limit]


@register.simple_tag
def get_popular_posts(limit=5):
    """Get most popular posts by view count."""
    from blog.models import Post
    
    return Post.objects.published().order_by('-views_count', '-created_at')[:limit]


@register.simple_tag
def get_recent_posts(limit=5):
    """Get most recent posts."""
    from blog.models import Post
    
    return Post.objects.published().order_by('-created_at')[:limit]


@register.simple_tag
def get_featured_posts(limit=3):
    """Get featured posts."""
    from blog.models import Post
    
    return Post.objects.published().filter(is_featured=True).order_by('-created_at')[:limit]


@register.inclusion_tag('blog/partials/post_card.html')
def render_post_card(post, show_excerpt=True, show_author=True):
    """Render a post card component."""
    return {
        'post': post,
        'show_excerpt': show_excerpt,
        'show_author': show_author,
    }


@register.simple_tag
def post_url(post):
    """Get the absolute URL for a post."""
    if not post:
        return '#'
    return reverse('blog:post_detail', kwargs={'slug': post.slug})


@register.simple_tag
def category_url(category):
    """Get the absolute URL for a category."""
    if not category:
        return '#'
    return reverse('blog:category_posts', kwargs={'slug': category.slug})


@register.simple_tag
def tag_url(tag):
    """Get the absolute URL for a tag."""
    if not tag:
        return '#'
    return reverse('blog:tag_posts', kwargs={'slug': tag.slug})


@register.filter
def add_css_class(field, css_class):
    """Add CSS class to form field."""
    return field.as_widget(attrs={'class': css_class})


@register.filter
def add_class(field, css_class):
    """Add CSS class to form field (alias for add_css_class)."""
    return add_css_class(field, css_class)


@register.filter
def build_absolute_uri(path, request):
    """Build absolute URI from path using request."""
    if not path or not request:
        return path
    return request.build_absolute_uri(path)


@register.simple_tag
def get_archive_months():
    """Get months with published posts for archive."""
    from blog.models import Post
    from django.db.models import Count
    from django.utils import timezone
    
    return (Post.objects.published()
            .extra({'month': "date_trunc('month', created_at)"})
            .values('month')
            .annotate(count=Count('id'))
            .order_by('-month')[:12])


@register.filter
def social_share_url(post, platform):
    """Generate social media share URLs."""
    if not post:
        return '#'
    
    post_url = post.get_absolute_url()
    post_title = post.title
    
    urls = {
        'twitter': f'https://twitter.com/intent/tweet?text={post_title}&url={post_url}',
        'facebook': f'https://www.facebook.com/sharer/sharer.php?u={post_url}',
        'linkedin': f'https://www.linkedin.com/sharing/share-offsite/?url={post_url}',
        'whatsapp': f'https://wa.me/?text={post_title} {post_url}',
    }
    
    return urls.get(platform, '#')


@register.simple_tag
def get_post_meta(post):
    """Get post metadata for structured data."""
    if not post:
        return {}
    
    return {
        'title': post.title,
        'description': post.excerpt or post.meta_description,
        'author': post.author.get_full_name() or post.author.username,
        'published_time': post.published_at or post.created_at,
        'modified_time': post.updated_at,
        'category': post.category.name if post.category else None,
        'tags': [tag.name for tag in post.tags.all()],
        'reading_time': post.reading_time,
        'url': post.get_absolute_url(),
    }