from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponse
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Project, ContactMessage, SiteSettings
from .forms import ContactForm
from blog.models import Post, Category
from taggit.models import Tag


def home(request):
    """Home page view."""
    # Get featured projects
    featured_projects = Project.objects.filter(is_featured=True)[:3]
    
    # Get latest blog posts
    latest_posts = Post.objects.filter(is_published=True)[:3]
    
    context = {
        'featured_projects': featured_projects,
        'latest_posts': latest_posts,
    }
    return render(request, 'core/home.html', context)


def about(request):
    """About page view."""
    return render(request, 'core/about.html')


def contact(request):
    """Contact page view."""
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save message to database
            contact_message = ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            
            # Send email notification
            try:
                send_mail(
                    subject=f"رسالة جديدة من الموقع: {form.cleaned_data['subject']}",
                    message=f"""اسم المرسل: {form.cleaned_data['name']}
البريد الإلكتروني: {form.cleaned_data['email']}
الموضوع: {form.cleaned_data['subject']}

الرسالة:
{form.cleaned_data['message']}""",
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.DEFAULT_FROM_EMAIL],
                    fail_silently=True,
                )
            except Exception as e:
                pass  # Handle email sending errors gracefully
            
            messages.success(request, _('تم إرسال رسالتك بنجاح. سأتواصل معك قريباً!'))
            return redirect('core:contact')
    else:
        form = ContactForm()
    
    return render(request, 'core/contact.html', {'form': form})


class ProjectListView(ListView):
    """Projects list view."""
    model = Project
    template_name = 'core/projects.html'
    context_object_name = 'projects'
    paginate_by = 9
    
    def get_queryset(self):
        return Project.objects.all()


class ProjectDetailView(DetailView):
    """Project detail view."""
    model = Project
    template_name = 'core/project_detail.html'
    context_object_name = 'project'
    slug_field = 'slug'
    slug_url_kwarg = 'slug'


def privacy_policy(request):
    """Privacy policy page."""
    return render(request, 'core/privacy_policy.html')


def terms_of_service(request):
    """Terms of service page."""
    return render(request, 'core/terms_of_service.html')


def robots_txt(request):
    """Robots.txt view."""
    lines = [
        "User-agent: *",
        "Allow: /",
        "Disallow: /admin/",
        "Disallow: /media/private/",
        "",
        f"Sitemap: {request.build_absolute_uri('/sitemap.xml')}",
    ]
    return HttpResponse("\n".join(lines), content_type="text/plain")


# Custom error views
def custom_404(request, exception):
    """Custom 404 error page."""
    return render(request, 'errors/404.html', status=404)


def custom_500(request):
    """Custom 500 error page."""
    return render(request, 'errors/500.html', status=500)


def custom_403(request, exception):
    """Custom 403 error page."""
    return render(request, 'errors/403.html', status=403)


def custom_405(request, exception):
    """Custom 405 error page."""
    return render(request, 'errors/405.html', status=405)


def global_search(request):
    """Global search view for posts and projects."""
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'all')  # all, posts, projects
    category_slug = request.GET.get('category', '')
    
    posts = []
    projects = []
    
    if query:
        # Search in blog posts
        if search_type in ['all', 'posts']:
            posts_queryset = Post.objects.published().select_related('author', 'category').prefetch_related('tags')
            posts_queryset = posts_queryset.filter(
                Q(title__icontains=query) |
                Q(excerpt__icontains=query) |
                Q(content__icontains=query) |
                Q(tags__name__icontains=query)
            ).distinct()
            
            if category_slug:
                posts_queryset = posts_queryset.filter(category__slug=category_slug)
            
            posts = posts_queryset[:6]  # Limit results
        
        # Search in projects
        if search_type in ['all', 'projects']:
            projects_queryset = Project.objects.all()
            projects_queryset = projects_queryset.filter(
                Q(title__icontains=query) |
                Q(short_description__icontains=query) |
                Q(description__icontains=query) |
                Q(technologies__icontains=query)
            ).distinct()
            
            projects = projects_queryset[:6]  # Limit results
    
    # Get categories for filter
    categories = Category.objects.filter(posts__is_published=True).distinct()
    
    # Calculate total results
    total_results = len(posts) + len(projects)
    
    context = {
        'query': query,
        'search_type': search_type,
        'category_slug': category_slug,
        'posts': posts,
        'projects': projects,
        'categories': categories,
        'total_results': total_results,
        'posts_count': len(posts),
        'projects_count': len(projects),
    }
    
    return render(request, 'core/global_search.html', context)