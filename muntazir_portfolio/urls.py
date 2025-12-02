"""URL configuration for muntazir_portfolio project."""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls.i18n import i18n_patterns
from django.contrib.sitemaps.views import sitemap
from django.views.i18n import set_language
from blog.sitemaps import PostSitemap
from core.sitemaps import StaticViewSitemap

# Sitemaps
sitemaps = {
    'posts': PostSitemap,
    'static': StaticViewSitemap,
}

# Non-internationalized URLs
urlpatterns = [
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
    path('i18n/setlang/', set_language, name='set_language'),
]

# Internationalized URLs
urlpatterns += i18n_patterns(
    path('', include('core.urls')),
    path('blog/', include('blog.urls')),
    path('books/', include('books.urls')),
    path('accounts/', include('accounts.urls')),
    prefix_default_language=True,
)

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Debug toolbar
    if 'debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns

# Custom error handlers
handler404 = 'core.views.custom_404'
handler500 = 'core.views.custom_500'
handler403 = 'core.views.custom_403'
handler405 = 'core.views.custom_405'