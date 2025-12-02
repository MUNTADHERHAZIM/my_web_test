from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, SetPasswordForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Submit, Div, HTML, Row, Column
from crispy_forms.bootstrap import FormActions
from .models import UserProfile
import re


class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form."""
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Enter your email')
        }),
        label=_('Email')
    )
    
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Enter your first name')
        }),
        label=_('First Name')
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Enter your last name')
        }),
        label=_('Last Name')
    )
    
    terms_accepted = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
        }),
        label=_('I agree to the Terms of Service and Privacy Policy')
    )
    
    # Honeypot field for spam protection
    honeypot = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label=''
    )
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('Choose a username')
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update password field widgets
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Enter your password')
        })
        
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Confirm your password')
        })
        
        # Update help texts
        self.fields['username'].help_text = _('Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.')
        self.fields['password1'].help_text = _('Your password must contain at least 8 characters.')
        self.fields['password2'].help_text = _('Enter the same password as before, for verification.')
        
        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        
        self.helper.layout = Layout(
            Field('honeypot'),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('username'),
            Field('email'),
            Field('password1'),
            Field('password2'),
            Field('terms_accepted'),
            FormActions(
                Submit(
                    'submit',
                    _('Create Account'),
                    css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200'
                )
            )
        )
    
    def clean_honeypot(self):
        """Check honeypot field for spam."""
        honeypot = self.cleaned_data.get('honeypot')
        if honeypot:
            raise ValidationError(_('Spam detected.'))
        return honeypot
    
    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise ValidationError(_('A user with this email already exists.'))
        return email
    
    def clean_username(self):
        """Validate username."""
        username = self.cleaned_data.get('username')
        
        if username:
            # Check for reserved usernames
            reserved_usernames = [
                'admin', 'administrator', 'root', 'api', 'www', 'mail',
                'ftp', 'blog', 'support', 'help', 'info', 'contact'
            ]
            
            if username.lower() in reserved_usernames:
                raise ValidationError(_('This username is reserved.'))
            
            # Check username pattern
            if not re.match(r'^[a-zA-Z0-9_]+$', username):
                raise ValidationError(_('Username can only contain letters, numbers, and underscores.'))
        
        return username
    
    def save(self, commit=True):
        """Save user with additional fields."""
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create user profile
            UserProfile.objects.create(user=user)
        
        return user


class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form."""
    
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
        }),
        label=_('Remember me')
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update field widgets
        self.fields['username'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Username or Email'),
            'autofocus': True
        })
        
        self.fields['password'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Password')
        })
        
        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        
        self.helper.layout = Layout(
            Field('username'),
            Field('password'),
            Field('remember_me'),
            FormActions(
                Submit(
                    'submit',
                    _('Sign In'),
                    css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200'
                )
            )
        )


class UserProfileForm(forms.ModelForm):
    """User profile form."""
    
    # User fields
    first_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white'
        }),
        label=_('First Name')
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white'
        }),
        label=_('Last Name')
    )
    
    email = forms.EmailField(
        required=False,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white'
        }),
        label=_('Email')
    )
    
    class Meta:
        model = UserProfile
        fields = [
            'bio', 'avatar', 'birth_date', 'phone', 'website',
            'country', 'city', 'twitter', 'linkedin', 'github',
            'language', 'timezone', 'show_email', 'show_phone',
            'email_notifications', 'newsletter_subscription'
        ]
        
        widgets = {
            'bio': forms.Textarea(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'rows': 4,
                'placeholder': _('Tell us about yourself...')
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-full file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 dark:file:bg-gray-700 dark:file:text-gray-300',
                'accept': 'image/*'
            }),
            'birth_date': forms.DateInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'type': 'date'
            }),
            'phone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('Phone number')
            }),
            'website': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': 'https://example.com'
            }),
            'country': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('Country')
            }),
            'city': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('City')
            }),
            'twitter': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('Twitter username (without @)')
            }),
            'linkedin': forms.URLInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': 'https://linkedin.com/in/username'
            }),
            'github': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': _('GitHub username')
            }),
            'language': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white'
            }),
            'timezone': forms.TextInput(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
                'placeholder': 'UTC'
            }),
            'show_email': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            }),
            'show_phone': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            }),
            'email_notifications': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            }),
            'newsletter_subscription': forms.CheckboxInput(attrs={
                'class': 'w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 rounded focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Set initial values from user
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
        
        # Crispy forms helper
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_enctype = 'multipart/form-data'
        self.helper.form_class = 'space-y-6'
        
        self.helper.layout = Layout(
            HTML('<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4">' + str(_('Personal Information')) + '</h3>'),
            Row(
                Column('first_name', css_class='form-group col-md-6 mb-0'),
                Column('last_name', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Field('email'),
            Field('bio'),
            Field('avatar'),
            Row(
                Column('birth_date', css_class='form-group col-md-6 mb-0'),
                Column('phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4 mt-6">' + str(_('Location')) + '</h3>'),
            Row(
                Column('country', css_class='form-group col-md-6 mb-0'),
                Column('city', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4 mt-6">' + str(_('Social Media & Website')) + '</h3>'),
            Field('website'),
            Row(
                Column('twitter', css_class='form-group col-md-4 mb-0'),
                Column('linkedin', css_class='form-group col-md-4 mb-0'),
                Column('github', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4 mt-6">' + str(_('Preferences')) + '</h3>'),
            Row(
                Column('language', css_class='form-group col-md-6 mb-0'),
                Column('timezone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            HTML('<h3 class="text-lg font-medium text-gray-900 dark:text-white mb-4 mt-6">' + str(_('Privacy & Notifications')) + '</h3>'),
            Row(
                Column('show_email', css_class='form-group col-md-6 mb-0'),
                Column('show_phone', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('email_notifications', css_class='form-group col-md-6 mb-0'),
                Column('newsletter_subscription', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            
            FormActions(
                Submit(
                    'submit',
                    _('Update Profile'),
                    css_class='bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-6 rounded-lg transition-colors duration-200'
                )
            )
        )
    
    def clean_email(self):
        """Validate email uniqueness."""
        email = self.cleaned_data.get('email')
        if email and self.instance.user:
            # Check if email is taken by another user
            if User.objects.filter(email=email).exclude(id=self.instance.user.id).exists():
                raise ValidationError(_('A user with this email already exists.'))
        return email
    
    def clean_avatar(self):
        """Validate avatar file."""
        avatar = self.cleaned_data.get('avatar')
        
        if avatar:
            # Check file size (max 5MB)
            if avatar.size > 5 * 1024 * 1024:
                raise ValidationError(_('Avatar file size cannot exceed 5MB.'))
            
            # Check file type
            allowed_types = ['image/jpeg', 'image/png', 'image/gif', 'image/webp']
            if avatar.content_type not in allowed_types:
                raise ValidationError(_('Avatar must be a JPEG, PNG, GIF, or WebP image.'))
        
        return avatar
    
    def save(self, commit=True):
        """Save profile and update user fields."""
        profile = super().save(commit=False)
        
        if commit:
            # Update user fields
            user = profile.user
            user.first_name = self.cleaned_data.get('first_name', '')
            user.last_name = self.cleaned_data.get('last_name', '')
            user.email = self.cleaned_data.get('email', '')
            user.save()
            
            # Save profile
            profile.save()
        
        return profile


class CustomPasswordResetForm(forms.Form):
    """Custom password reset form."""
    
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Enter your email address')
        }),
        label=_('Email')
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        
        self.helper.layout = Layout(
            Field('email'),
            FormActions(
                Submit(
                    'submit',
                    _('Send Reset Link'),
                    css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200'
                )
            )
        )


class CustomSetPasswordForm(SetPasswordForm):
    """Custom set password form."""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Update field widgets
        self.fields['new_password1'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Enter new password')
        })
        
        self.fields['new_password2'].widget.attrs.update({
            'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent dark:bg-gray-700 dark:border-gray-600 dark:text-white',
            'placeholder': _('Confirm new password')
        })
        
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.form_class = 'space-y-4'
        
        self.helper.layout = Layout(
            Field('new_password1'),
            Field('new_password2'),
            FormActions(
                Submit(
                    'submit',
                    _('Set New Password'),
                    css_class='w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors duration-200'
                )
            )
        )