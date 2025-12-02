from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Q, Count
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from .models import Book, BookCategory, BookNote
from .forms import BookForm, BookNoteForm


class BookListView(ListView):
    """List all published books."""
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.filter(is_published=True).select_related('category', 'added_by')
        
        # Search functionality
        search_query = self.request.GET.get('search')
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        
        # Filter by category
        category_slug = self.request.GET.get('category')
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Filter by rating
        rating = self.request.GET.get('rating')
        if rating:
            queryset = queryset.filter(rating=rating)
        
        # Sorting
        sort_by = self.request.GET.get('sort', '-created_at')
        if sort_by in ['title', '-title', 'author', '-author', 'rating', '-rating', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = BookCategory.objects.annotate(book_count=Count('books')).filter(book_count__gt=0)
        context['search_query'] = self.request.GET.get('search', '')
        context['selected_category'] = self.request.GET.get('category', '')
        context['selected_status'] = self.request.GET.get('status', '')
        context['selected_rating'] = self.request.GET.get('rating', '')
        context['sort_by'] = self.request.GET.get('sort', '-created_at')
        return context


class BookDetailView(DetailView):
    """Display book details."""
    model = Book
    template_name = 'books/book_detail.html'
    context_object_name = 'book'
    
    def get_queryset(self):
        return Book.objects.filter(is_published=True).select_related('category', 'added_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['notes'] = self.object.notes.all().order_by('-created_at')
        context['related_books'] = Book.objects.filter(
            category=self.object.category,
            is_published=True
        ).exclude(id=self.object.id)[:4]
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    """Create a new book."""
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def form_valid(self, form):
        form.instance.added_by = self.request.user
        messages.success(self.request, _('Book added successfully!'))
        return super().form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    """Update an existing book."""
    model = Book
    form_class = BookForm
    template_name = 'books/book_form.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def get_queryset(self):
        return Book.objects.filter(added_by=self.request.user)
    
    def form_valid(self, form):
        messages.success(self.request, _('Book updated successfully!'))
        return super().form_valid(form)


class BookDeleteView(LoginRequiredMixin, DeleteView):
    """Delete a book."""
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('accounts:dashboard')
    
    def get_queryset(self):
        return Book.objects.filter(added_by=self.request.user)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, _('Book deleted successfully!'))
        return super().delete(request, *args, **kwargs)


class BookCategoryListView(ListView):
    """List all book categories."""
    model = BookCategory
    template_name = 'books/category_list.html'
    context_object_name = 'categories'
    
    def get_queryset(self):
        return BookCategory.objects.annotate(book_count=Count('books')).filter(book_count__gt=0)


class CategoryBooksView(ListView):
    """List books in a specific category."""
    model = Book
    template_name = 'books/category_books.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        self.category = get_object_or_404(BookCategory, slug=self.kwargs['slug'])
        return Book.objects.filter(
            category=self.category,
            is_published=True
        ).select_related('category', 'added_by')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class BookNoteCreateView(LoginRequiredMixin, CreateView):
    """Create a note for a book."""
    model = BookNote
    form_class = BookNoteForm
    template_name = 'books/note_form.html'
    
    def get_success_url(self):
        return self.object.book.get_absolute_url()
    
    def form_valid(self, form):
        book = get_object_or_404(Book, slug=self.kwargs['book_slug'])
        form.instance.book = book
        messages.success(self.request, _('Note added successfully!'))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['book'] = get_object_or_404(Book, slug=self.kwargs['book_slug'])
        return context


class MyBooksView(LoginRequiredMixin, ListView):
    """List user's books."""
    model = Book
    template_name = 'books/my_books.html'
    context_object_name = 'books'
    paginate_by = 12
    
    def get_queryset(self):
        queryset = Book.objects.filter(added_by=self.request.user)
        
        # Filter by status
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        return queryset.order_by('-created_at')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['selected_status'] = self.request.GET.get('status', '')
        context['status_counts'] = {
            'all': self.request.user.books.count(),
            'reading': self.request.user.books.filter(status='reading').count(),
            'completed': self.request.user.books.filter(status='completed').count(),
            'want_to_read': self.request.user.books.filter(status='want_to_read').count(),
            'abandoned': self.request.user.books.filter(status='abandoned').count(),
        }
        return context