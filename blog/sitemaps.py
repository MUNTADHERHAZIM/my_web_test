from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Post, Category
from taggit.models import Tag


class PostSitemap(Sitemap):
    """Sitemap for blog posts."""
    
    changefreq = 'weekly'
    priority = 0.8
    
    def items(self):
        """Return all published posts."""
        return Post.published.all()
    
    def lastmod(self, obj):
        """Return last modification date."""
        return obj.updated_at
    
    def location(self, obj):
        """Return post URL."""
        return reverse('blog:post_detail', args=[obj.slug])


class CategorySitemap(Sitemap):
    """Sitemap for blog categories."""
    
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        """Return all categories that have published posts."""
        return Category.objects.filter(posts__is_published=True).distinct()
    
    def lastmod(self, obj):
        """Return last modification date based on latest post in category."""
        latest_post = obj.posts.filter(is_published=True).order_by('-updated_at').first()
        return latest_post.updated_at if latest_post else obj.created_at
    
    def location(self, obj):
        """Return category URL."""
        return reverse('blog:category_posts', args=[obj.slug])


class TagSitemap(Sitemap):
    """Sitemap for blog tags."""
    
    changefreq = 'monthly'
    priority = 0.5
    
    def items(self):
        """Return all tags that have published posts."""
        return Tag.objects.filter(
            taggit_taggeditem_items__content_type__model='post',
            taggit_taggeditem_items__object_id__in=Post.published.values_list('id', flat=True)
        ).distinct()
    
    def lastmod(self, obj):
        """Return last modification date based on latest post with this tag."""
        latest_post = Post.published.filter(tags__in=[obj]).order_by('-updated_at').first()
        return latest_post.updated_at if latest_post else None
    
    def location(self, obj):
        """Return tag URL."""
        return reverse('blog:tag_posts', args=[obj.slug])


class BlogStaticSitemap(Sitemap):
    """Sitemap for static blog pages."""
    
    changefreq = 'monthly'
    priority = 0.7
    
    def items(self):
        """Return static blog pages."""
        return ['blog:post_list', 'blog:archive']
    
    def location(self, item):
        """Return URL for static pages."""
        return reverse(item)