from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.db.models import Q, Count
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.utils.translation import gettext_lazy as _
from django.http import Http404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from taggit.models import Tag
from .models import Post, Category, Comment
from .forms import CommentForm, PostForm


class PostListView(ListView):
    """Blog posts list view."""
    model = Post
    template_name = 'blog/post_list.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        queryset = Post.objects.published().select_related('author', 'category').prefetch_related('tags')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(excerpt__icontains=search_query) |
                Q(content__icontains=search_query) |
                Q(tags__name__icontains=search_query)
            ).distinct()
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_query'] = self.request.GET.get('search', '')
        context['categories'] = Category.objects.annotate(
            post_count=Count('posts', filter=Q(posts__is_published=True))
        ).filter(post_count__gt=0)
        context['popular_tags'] = Tag.objects.annotate(
            post_count=Count('taggit_taggeditem_items')
        ).filter(post_count__gt=0).order_by('-post_count')[:10]
        return context


class PostDetailView(DetailView):
    """Blog post detail view."""
    model = Post
    template_name = 'blog/post_detail.html'
    context_object_name = 'post'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Post.objects.published().select_related('author', 'category').prefetch_related('tags')
    
    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        # Increment views count
        obj.increment_views()
        return obj
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get related posts
        context['related_posts'] = post.get_related_posts()
        
        # Get previous and next posts
        context['previous_post'] = Post.objects.published().filter(
            published_at__lt=post.published_at
        ).first()
        context['next_post'] = Post.objects.published().filter(
            published_at__gt=post.published_at
        ).order_by('published_at').first()
        
        # Get approved comments
        context['comments'] = post.comments.filter(is_approved=True).order_by('-created_at')
        
        # Add comment form
        context['comment_form'] = CommentForm()
        
        return context


class CategoryPostsView(ListView):
    """Posts by category view."""
    model = Post
    template_name = 'blog/category_posts.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return Post.objects.published().filter(category=self.category).select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class TagPostsView(ListView):
    """Posts by tag view."""
    model = Post
    template_name = 'blog/tag_posts.html'
    context_object_name = 'posts'
    paginate_by = 9
    
    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Post.objects.published().filter(tags=self.tag).select_related('author', 'category').prefetch_related('tags')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


def archive_view(request, year=None, month=None):
    """Archive view for posts by year/month."""
    posts = Post.objects.published().select_related('author', 'category').prefetch_related('tags')
    
    if year:
        posts = posts.filter(published_at__year=year)
        if month:
            posts = posts.filter(published_at__month=month)
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'year': year,
        'month': month,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
    }
    
    return render(request, 'blog/archive.html', context)


def search_view(request):
    """Advanced search view."""
    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    tag_slug = request.GET.get('tag', '')
    
    posts = Post.objects.published().select_related('author', 'category').prefetch_related('tags')
    
    if query:
        posts = posts.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        ).distinct()
    
    if category_slug:
        posts = posts.filter(category__slug=category_slug)
    
    if tag_slug:
        posts = posts.filter(tags__slug=tag_slug)
    
    # Pagination
    paginator = Paginator(posts, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    # Get categories and tags for filters
    categories = Category.objects.annotate(
        post_count=Count('posts', filter=Q(posts__is_published=True))
    ).filter(post_count__gt=0)
    
    popular_tags = Tag.objects.annotate(
        post_count=Count('taggit_taggeditem_items')
    ).filter(post_count__gt=0).order_by('-post_count')[:20]
    
    context = {
        'posts': page_obj,
        'query': query,
        'category_slug': category_slug,
        'tag_slug': tag_slug,
        'categories': categories,
        'popular_tags': popular_tags,
        'page_obj': page_obj,
        'is_paginated': page_obj.has_other_pages(),
        'results_count': posts.count(),
    }
    
    return render(request, 'blog/search.html', context)


@login_required
def add_comment(request, slug):
    """Add a comment to a blog post."""
    post = get_object_or_404(Post, slug=slug, is_published=True)
    
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        website = request.POST.get('website', '').strip()
        content = request.POST.get('content', '').strip()
        
        if name and email and content:
            comment = Comment.objects.create(
                post=post,
                name=name,
                email=email,
                website=website,
                content=content,
                is_approved=False  # Comments need approval
            )
            messages.success(request, _('Your comment has been submitted and is awaiting approval.'))
        else:
            messages.error(request, _('Please fill in all required fields.'))
    
    return redirect('blog:post_detail', slug=slug)


class PostCreateView(LoginRequiredMixin, CreateView):
    """Create a new blog post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing blog post."""
    model = Post
    form_class = PostForm
    template_name = 'blog/post_form.html'
    success_url = reverse_lazy('accounts:dashboard')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)


class PostDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a blog post."""
    model = Post
    template_name = 'blog/post_confirm_delete.html'
    success_url = reverse_lazy('accounts:dashboard')
    slug_field = 'slug'
    slug_url_kwarg = 'slug'
    
    def get_queryset(self):
        return Post.objects.filter(author=self.request.user)