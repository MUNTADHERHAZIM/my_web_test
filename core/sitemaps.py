from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Project


class StaticViewSitemap(Sitemap):
    """Sitemap for static pages."""
    priority = 0.8
    changefreq = 'weekly'
    
    def items(self):
        return ['core:home', 'core:about', 'core:contact', 'core:projects']
    
    def location(self, item):
        return reverse(item)


class ProjectSitemap(Sitemap):
    """Sitemap for projects."""
    changefreq = 'monthly'
    priority = 0.6
    
    def items(self):
        return Project.objects.all()
    
    def lastmod(self, obj):
        return obj.updated_at