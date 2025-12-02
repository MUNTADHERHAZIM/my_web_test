from django.contrib.syndication.views import Feed
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.utils.feedgenerator import Atom1Feed
from django.conf import settings
from .models import Post


class LatestPostsFeed(Feed):
    """RSS feed for latest blog posts."""
    
    title = _("Muntazir Hazim Thamer - Latest Blog Posts")
    link = "/blog/"
    description = _("Latest articles and insights from Muntazir Hazim Thamer's blog")
    
    def items(self):
        """Return latest 10 published posts."""
        return Post.published.select_related('author', 'category').prefetch_related('tags')[:10]
    
    def item_title(self, item):
        """Return post title."""
        return item.title
    
    def item_description(self, item):
        """Return post excerpt or truncated content."""
        return item.excerpt or item.get_excerpt()
    
    def item_link(self, item):
        """Return post absolute URL."""
        return reverse('blog:post_detail', args=[item.slug])
    
    def item_pubdate(self, item):
        """Return post publication date."""
        return item.published_at
    
    def item_updateddate(self, item):
        """Return post last update date."""
        return item.updated_at
    
    def item_author_name(self, item):
        """Return post author name."""
        return item.author.get_full_name() or item.author.username
    
    def item_author_email(self, item):
        """Return post author email."""
        return item.author.email
    
    def item_categories(self, item):
        """Return post categories and tags."""
        categories = [item.category.name] if item.category else []
        tags = [tag.name for tag in item.tags.all()]
        return categories + tags
    
    def item_guid(self, item):
        """Return unique identifier for the item."""
        return f"post-{item.id}-{item.slug}"
    
    def item_guid_is_permalink(self, item):
        """Indicate that GUID is not a permalink."""
        return False


class LatestPostsAtomFeed(LatestPostsFeed):
    """Atom feed for latest blog posts."""
    
    feed_type = Atom1Feed
    subtitle = LatestPostsFeed.description


class CategoryFeed(Feed):
    """RSS feed for posts in a specific category."""
    
    def get_object(self, request, slug):
        """Get category object from URL."""
        from .models import Category
        return Category.objects.get(slug=slug)
    
    def title(self, obj):
        """Return feed title with category name."""
        return _("Muntazir Hazim Thamer - {} Posts").format(obj.name)
    
    def link(self, obj):
        """Return category URL."""
        return reverse('blog:category_posts', args=[obj.slug])
    
    def description(self, obj):
        """Return feed description with category."""
        return _("Latest posts in {} category").format(obj.name)
    
    def items(self, obj):
        """Return latest posts in category."""
        return Post.published.filter(category=obj).select_related('author', 'category').prefetch_related('tags')[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.excerpt or item.get_excerpt()
    
    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.slug])
    
    def item_pubdate(self, item):
        return item.published_at
    
    def item_updateddate(self, item):
        return item.updated_at
    
    def item_author_name(self, item):
        return item.author.get_full_name() or item.author.username
    
    def item_categories(self, item):
        categories = [item.category.name] if item.category else []
        tags = [tag.name for tag in item.tags.all()]
        return categories + tags


class TagFeed(Feed):
    """RSS feed for posts with a specific tag."""
    
    def get_object(self, request, slug):
        """Get tag object from URL."""
        from taggit.models import Tag
        return Tag.objects.get(slug=slug)
    
    def title(self, obj):
        """Return feed title with tag name."""
        return _("Muntazir Hazim Thamer - Posts tagged '{}'").format(obj.name)
    
    def link(self, obj):
        """Return tag URL."""
        return reverse('blog:tag_posts', args=[obj.slug])
    
    def description(self, obj):
        """Return feed description with tag."""
        return _("Latest posts tagged with '{}'").format(obj.name)
    
    def items(self, obj):
        """Return latest posts with tag."""
        return Post.published.filter(tags__in=[obj]).select_related('author', 'category').prefetch_related('tags')[:10]
    
    def item_title(self, item):
        return item.title
    
    def item_description(self, item):
        return item.excerpt or item.get_excerpt()
    
    def item_link(self, item):
        return reverse('blog:post_detail', args=[item.slug])
    
    def item_pubdate(self, item):
        return item.published_at
    
    def item_updateddate(self, item):
        return item.updated_at
    
    def item_author_name(self, item):
        return item.author.get_full_name() or item.author.username
    
    def item_categories(self, item):
        categories = [item.category.name] if item.category else []
        tags = [tag.name for tag in item.tags.all()]
        return categories + tags