from django import forms
from django.utils.translation import gettext_lazy as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """Contact form with honeypot protection."""
    
    # Honeypot field (hidden from users, bots might fill it)
    website = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label=''
    )
    
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('اسمك الكامل')
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('بريدك الإلكتروني')
            }),
            'subject': forms.TextInput(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('موضوع الرسالة')
            }),
            'message': forms.Textarea(attrs={
                'class': 'w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('اكتب رسالتك هنا...'),
                'rows': 6
            }),
        }
        labels = {
            'name': _('الاسم'),
            'email': _('البريد الإلكتروني'),
            'subject': _('الموضوع'),
            'message': _('الرسالة'),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-6'
        
        self.helper.layout = Layout(
            Field('website'),  # Honeypot field
            Div(
                Field('name'),
                css_class='space-y-2'
            ),
            Div(
                Field('email'),
                css_class='space-y-2'
            ),
            Div(
                Field('subject'),
                css_class='space-y-2'
            ),
            Div(
                Field('message'),
                css_class='space-y-2'
            ),
            Submit(
                'submit',
                _('إرسال الرسالة'),
                css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-6 rounded-lg transition duration-300 ease-in-out transform hover:scale-105'
            )
        )
    
    def clean_website(self):
        """Honeypot validation - if filled, it's likely a bot."""
        website = self.cleaned_data.get('website')
        if website:
            raise forms.ValidationError(_('Bot detected!'))
        return website
    
    def clean_name(self):
        """Validate name field."""
        name = self.cleaned_data.get('name')
        if len(name) < 2:
            raise forms.ValidationError(_('الاسم يجب أن يكون أكثر من حرفين.'))
        return name
    
    def clean_message(self):
        """Validate message field."""
        message = self.cleaned_data.get('message')
        if len(message) < 10:
            raise forms.ValidationError(_('الرسالة يجب أن تكون أكثر من 10 أحرف.'))
        return message