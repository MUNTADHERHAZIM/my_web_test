from django.urls import path
from . import views
from . import upload_views
from .feeds import LatestPostsFeed

app_name = 'blog'

urlpatterns = [
    # Blog main pages
    path('', views.PostListView.as_view(), name='post_list'),
    path('search/', views.search_view, name='search'),
    
    # Post management (must come before post detail to avoid slug conflicts)
    path('post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('post/<slug:slug>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('post/<slug:slug>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Post detail
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<slug:slug>/comment/', views.add_comment, name='add_comment'),
    
    # Category and tag pages
    path('category/<slug:slug>/', views.CategoryPostsView.as_view(), name='category_posts'),
    path('tag/<str:slug>/', views.TagPostsView.as_view(), name='tag_posts'),
    
    # Archive pages
    path('archive/', views.archive_view, name='archive'),
    path('archive/<int:year>/', views.archive_view, name='archive_year'),
    path('archive/<int:year>/<int:month>/', views.archive_view, name='archive_month'),
    
    # RSS Feed
    path('rss/', LatestPostsFeed(), name='rss_feed'),
    
    # مسارات رفع الملفات
    path('upload/', upload_views.upload_file, name='upload_file'),
    path('browse/', upload_views.browse_files, name='browse_files'),
    path('delete-file/', upload_views.delete_file, name='delete_file'),
    path('file-info/', upload_views.get_file_info, name='file_info'),
]