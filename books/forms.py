from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, Row, Column
from .models import Book, BookNote, BookCategory


class BookForm(forms.ModelForm):
    """Form for creating and editing books."""
    
    class Meta:
        model = Book
        fields = [
            'title', 'author', 'isbn', 'description', 'review', 'cover_image',
            'pages', 'publication_date', 'publisher', 'language', 'category',
            'tags', 'status', 'rating', 'start_date', 'finish_date',
            'is_published', 'is_featured', 'meta_description', 'meta_keywords'
        ]
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Book title')
            }),
            'author': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Author name')
            }),
            'isbn': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('ISBN (optional)')
            }),
            'description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'rows': 4,
                'placeholder': _('Book description')
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'accept': 'image/*'
            }),
            'pages': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Number of pages')
            }),
            'publication_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'type': 'date'
            }),
            'publisher': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Publisher')
            }),
            'language': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Language')
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
            }),
            'rating': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
            }),
            'start_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'type': 'date'
            }),
            'finish_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'type': 'date'
            }),
            'meta_description': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'rows': 3,
                'placeholder': _('Meta description for SEO')
            }),
            'meta_keywords': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Meta keywords for SEO')
            }),
        }
        
        labels = {
            'title': _('Title'),
            'author': _('Author'),
            'isbn': _('ISBN'),
            'description': _('Description'),
            'review': _('Review'),
            'cover_image': _('Cover Image'),
            'pages': _('Pages'),
            'publication_date': _('Publication Date'),
            'publisher': _('Publisher'),
            'language': _('Language'),
            'category': _('Category'),
            'tags': _('Tags'),
            'status': _('Reading Status'),
            'rating': _('Rating'),
            'start_date': _('Start Date'),
            'finish_date': _('Finish Date'),
            'is_published': _('Published'),
            'is_featured': _('Featured'),
            'meta_description': _('Meta Description'),
            'meta_keywords': _('Meta Keywords'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        
        # Make some fields optional in the form
        self.fields['isbn'].required = False
        self.fields['description'].required = False
        self.fields['review'].required = False
        self.fields['cover_image'].required = False
        self.fields['pages'].required = False
        self.fields['publication_date'].required = False
        self.fields['publisher'].required = False
        self.fields['category'].required = False
        self.fields['rating'].required = False
        self.fields['start_date'].required = False
        self.fields['finish_date'].required = False
        self.fields['meta_description'].required = False
        self.fields['meta_keywords'].required = False


class BookNoteForm(forms.ModelForm):
    """Form for creating book notes."""
    
    class Meta:
        model = BookNote
        fields = ['title', 'content', 'page_number', 'is_quote', 'is_favorite']
        
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Note title (optional)')
            }),
            'page_number': forms.NumberInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Page number (optional)')
            }),
        }
        
        labels = {
            'title': _('Title'),
            'content': _('Content'),
            'page_number': _('Page Number'),
            'is_quote': _('This is a quote'),
            'is_favorite': _('Mark as favorite'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        
        # Make some fields optional
        self.fields['title'].required = False
        self.fields['page_number'].required = False


class BookSearchForm(forms.Form):
    """Form for searching books."""
    
    search = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
            'placeholder': _('Search books by title, author, or description...')
        })
    )
    
    category = forms.ModelChoiceField(
        queryset=BookCategory.objects.all(),
        required=False,
        empty_label=_('All Categories'),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
        })
    )
    
    status = forms.ChoiceField(
        choices=[('', _('All Status'))] + Book.STATUS_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
        })
    )
    
    rating = forms.ChoiceField(
        choices=[('', _('All Ratings'))] + Book.RATING_CHOICES,
        required=False,
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
        })
    )
    
    sort = forms.ChoiceField(
        choices=[
            ('-created_at', _('Newest First')),
            ('created_at', _('Oldest First')),
            ('title', _('Title A-Z')),
            ('-title', _('Title Z-A')),
            ('author', _('Author A-Z')),
            ('-author', _('Author Z-A')),
            ('-rating', _('Highest Rated')),
            ('rating', _('Lowest Rated')),
        ],
        required=False,
        initial='-created_at',
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
        })
    )