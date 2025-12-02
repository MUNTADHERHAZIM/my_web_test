from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    # Book list
    path('', views.BookListView.as_view(), name='book_list'),
    
    # Book CRUD (create must come before detail to avoid slug conflicts)
    path('create/', views.BookCreateView.as_view(), name='book_create'),
    path('<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
    path('<slug:slug>/edit/', views.BookUpdateView.as_view(), name='book_edit'),
    path('<slug:slug>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    
    # Categories
    path('categories/', views.BookCategoryListView.as_view(), name='category_list'),
    path('category/<slug:slug>/', views.CategoryBooksView.as_view(), name='category_books'),
    
    # Notes
    path('<slug:book_slug>/note/add/', views.BookNoteCreateView.as_view(), name='note_create'),
    
    # User's books
    path('my-books/', views.MyBooksView.as_view(), name='my_books'),
]