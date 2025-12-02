from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from .models import Comment, Category, Post


class CommentForm(forms.ModelForm):
    """Form for adding comments to blog posts."""
    
    # Honeypot field for spam protection
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label=''
    )
    
    class Meta:
        model = Comment
        fields = ['name', 'email', 'website', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('Your name')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('Your email')
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('Your website (optional)')
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('Write your comment...'),
                'rows': 5
            })
        }
        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'website': _('Website'),
            'content': _('Comment')
        }
        help_texts = {
            'email': _('Your email will not be published.'),
            'website': _('Optional: Include your website URL.'),
            'content': _('Please be respectful and constructive in your comments.')
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        
        self.helper.layout = Layout(
            Field('honeypot'),
            Div(
                Field('name', wrapper_class='mb-4'),
                Field('email', wrapper_class='mb-4'),
                css_class='grid grid-cols-1 md:grid-cols-2 gap-4'
            ),
            Field('website', wrapper_class='mb-4'),
            Field('content', wrapper_class='mb-4'),
            FormActions(
                Submit(
                    'submit',
                    _('Post Comment'),
                    css_class='bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200'
                )
            )
        )
    
    def clean_honeypot(self):
        """Check honeypot field for spam."""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError(_('Spam detected.'))
        return honeypot


class PostForm(forms.ModelForm):
    """Form for creating and editing blog posts with CKEditor."""
    
    class Meta:
        model = Post
        fields = ['title', 'excerpt', 'content', 'cover_image', 'category', 'tags', 'is_published', 'is_featured']
        widgets = {
            'content': CKEditorUploadingWidget(config_name='default'),
            'title': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Enter post title')
            }),
            'excerpt': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Brief description of the post'),
                'rows': 3
            }),
            'cover_image': forms.FileInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
            }),
            'category': forms.Select(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white'
            }),
            'tags': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 focus:border-transparent dark:bg-gray-700 dark:text-white',
                'placeholder': _('Enter tags separated by commas')
            }),
        }
        labels = {
            'title': _('Title'),
            'excerpt': _('Excerpt'),
            'content': _('Content'),
            'cover_image': _('Cover Image'),
            'category': _('Category'),
            'tags': _('Tags'),
            'is_published': _('Published'),
            'is_featured': _('Featured'),
        }
        help_texts = {
            'excerpt': _('Brief description that will appear in post previews'),
            'tags': _('Enter tags separated by commas'),
            'is_published': _('Check to make this post visible to the public'),
            'is_featured': _('Featured posts appear prominently on the homepage'),
        }
    
    def clean_name(self):
        """Validate name field."""
        name = self.cleaned_data.get('name')
        if name and len(name) < 2:
            raise forms.ValidationError(_('Name must be at least 2 characters long.'))
        return name
    
    def clean_content(self):
        """Validate content field."""
        content = self.cleaned_data.get('content')
        if content and len(content) < 10:
            raise forms.ValidationError(_('Comment must be at least 10 characters long.'))
        return content


class SearchForm(forms.Form):
    """Form for searching blog posts."""
    
    query = forms.CharField(
        max_length=255,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Search posts...'),
            'autocomplete': 'off'
        }),
        label=_('Search')
    )
    
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label=_('All Categories'),
        widget=forms.Select(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white'
        }),
        label=_('Category')
    )
    
    tag = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Tag name...'),
            'autocomplete': 'off'
        }),
        label=_('Tag')
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.form_class = 'space-y-4'
        
        self.helper.layout = Layout(
            Field('query', wrapper_class='mb-4'),
            Div(
                Field('category', wrapper_class='mb-4'),
                Field('tag', wrapper_class='mb-4'),
                css_class='grid grid-cols-1 md:grid-cols-2 gap-4'
            ),
            FormActions(
                Submit(
                    'submit',
                    _('Search'),
                    css_class='bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200'
                ),
                HTML(
                    '<a href="{% url "blog:post_list" %}" class="ml-2 bg-gray-500 hover:bg-gray-600 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200 inline-block">' + str(_('Clear')) + '</a>'
                )
            )
        )
    
    def clean_query(self):
        """Clean and validate search query."""
        query = self.cleaned_data.get('query')
        if query:
            # Remove extra whitespace
            query = ' '.join(query.split())
            # Minimum length check
            if len(query) < 2:
                raise forms.ValidationError(_('Search query must be at least 2 characters long.'))
        return query


class NewsletterForm(forms.Form):
    """Simple newsletter subscription form."""
    
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-l-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Enter your email')
        }),
        label=''
    )
    
    # Honeypot field
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label=''
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'flex'
        self.helper.disable_csrf = False
        
        self.helper.layout = Layout(
            Field('honeypot'),
            Div(
                Field('email', wrapper_class='flex-1'),
                Submit(
                    'submit',
                    _('Subscribe'),
                    css_class='bg-blue-600 hover:bg-blue-700 text-white font-medium px-6 py-2 rounded-r-lg transition-colors duration-200'
                ),
                css_class='flex'
            )
        )
    
    def clean_honeypot(self):
        """Check honeypot field for spam."""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise forms.ValidationError(_('Spam detected.'))
        return honeypot