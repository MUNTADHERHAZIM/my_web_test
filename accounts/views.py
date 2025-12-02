from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import gettext_lazy as _
from django.http import JsonResponse, HttpResponseRedirect
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from django.db import transaction
from django.contrib.auth.forms import PasswordChangeForm
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from django.utils.decorators import method_decorator
from .models import UserProfile, LoginAttempt, PasswordResetToken
from .forms import (
    CustomUserCreationForm, UserProfileForm, CustomAuthenticationForm,
    CustomPasswordResetForm, CustomSetPasswordForm
)
import secrets
from datetime import timedelta


def get_client_ip(request):
    """Get client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def log_login_attempt(request, username, success=False):
    """Log login attempt for security tracking."""
    LoginAttempt.objects.create(
        username=username,
        ip_address=get_client_ip(request),
        user_agent=request.META.get('HTTP_USER_AGENT', ''),
        success=success
    )


class RegisterView(CreateView):
    """User registration view."""
    
    form_class = CustomUserCreationForm
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('accounts:login')
    
    def dispatch(self, request, *args, **kwargs):
        """Redirect authenticated users."""
        if request.user.is_authenticated:
            return redirect('core:home')
        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        """Handle valid form submission."""
        response = super().form_valid(form)
        
        # Log successful registration
        log_login_attempt(self.request, form.cleaned_data['username'], success=True)
        
        # Send welcome email
        try:
            send_mail(
                subject=_('Welcome to Muntazir Portfolio'),
                message=_('Thank you for registering! Welcome to our community.'),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.object.email],
                fail_silently=True
            )
        except Exception:
            pass  # Don't fail registration if email fails
        
        messages.success(
            self.request,
            _('Registration successful! You can now log in.')
        )
        
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Register')
        return context


@csrf_protect
def login_view(request):
    """Custom login view with security features."""
    
    if request.user.is_authenticated:
        return redirect('core:home')
    
    form = CustomAuthenticationForm()
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data.get('remember_me', False)
            
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Log successful login
                log_login_attempt(request, username, success=True)
                
                # Login user
                login(request, user)
                
                # Set session expiry based on remember me
                if not remember_me:
                    request.session.set_expiry(0)  # Browser session
                else:
                    request.session.set_expiry(1209600)  # 2 weeks
                
                messages.success(request, _('Welcome back!'))
                
                # Redirect to next or home
                next_url = request.GET.get('next', 'core:home')
                return redirect(next_url)
            else:
                # Log failed login
                log_login_attempt(request, username, success=False)
                messages.error(request, _('Invalid username or password.'))
        else:
            # Log failed login attempt
            username = request.POST.get('username', '')
            if username:
                log_login_attempt(request, username, success=False)
    
    context = {
        'form': form,
        'title': _('Login')
    }
    
    return render(request, 'accounts/login.html', context)


@login_required
def logout_view(request):
    """Logout view."""
    logout(request)
    messages.success(request, _('You have been logged out successfully.'))
    return redirect('core:home')


class MyProfileView(LoginRequiredMixin, DetailView):
    """Current user's profile view."""
    
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    
    def get_object(self, queryset=None):
        """Return the current user."""
        return self.request.user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        # Get or create user profile
        userprofile, created = UserProfile.objects.get_or_create(user=user)
        
        context.update({
            'profile': userprofile,
            'title': f"{user.get_full_name() or user.username}'s Profile",
            'is_own_profile': True,
            'social_links': userprofile.get_social_links(),
            'completion_percentage': userprofile.get_completion_percentage()
        })
        
        return context


class ProfileView(DetailView):
    """Public user profile view."""
    
    model = User
    template_name = 'accounts/profile.html'
    context_object_name = 'profile_user'
    slug_field = 'username'
    slug_url_kwarg = 'username'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.get_object()
        
        # Get or create user profile
        userprofile, created = UserProfile.objects.get_or_create(user=user)
        
        context.update({
            'profile': userprofile,
            'title': f"{user.get_full_name() or user.username}'s Profile",
            'is_own_profile': self.request.user == user,
            'social_links': userprofile.get_social_links(),
            'completion_percentage': userprofile.get_completion_percentage()
        })
        
        return context


class ProfileUpdateView(LoginRequiredMixin, UpdateView):
    """Update user profile view."""
    
    model = UserProfile
    form_class = UserProfileForm
    template_name = 'accounts/profile_edit.html'
    
    def get_object(self, queryset=None):
        """Get or create user profile."""
        userprofile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return userprofile
    
    def get_success_url(self):
        return reverse('accounts:profile', kwargs={'username': self.request.user.username})
    
    def form_valid(self, form):
        """Handle valid form submission."""
        messages.success(self.request, _('Profile updated successfully!'))
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Edit Profile')
        return context


@login_required
def change_password_view(request):
    """Change password view."""
    
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep user logged in
            messages.success(request, _('Password changed successfully!'))
            return redirect('accounts:profile', username=request.user.username)
    else:
        form = PasswordChangeForm(request.user)
    
    context = {
        'form': form,
        'title': _('Change Password')
    }
    
    return render(request, 'accounts/change_password.html', context)


def password_reset_request_view(request):
    """Password reset request view."""
    
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = CustomPasswordResetForm(request.POST)
        
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email, is_active=True)
                
                # Create reset token
                token = secrets.token_urlsafe(32)
                expires_at = timezone.now() + timedelta(hours=24)
                
                # Invalidate old tokens
                PasswordResetToken.objects.filter(user=user, used=False).update(used=True)
                
                # Create new token
                reset_token = PasswordResetToken.objects.create(
                    user=user,
                    token=token,
                    expires_at=expires_at
                )
                
                # Send reset email
                reset_url = request.build_absolute_uri(
                    reverse('accounts:password_reset_confirm', kwargs={'token': token})
                )
                
                send_mail(
                    subject=_('Password Reset Request'),
                    message=_('Click the following link to reset your password: {}').format(reset_url),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[email],
                    fail_silently=False
                )
                
                messages.success(
                    request,
                    _('Password reset email sent! Check your inbox.')
                )
                
                return redirect('accounts:login')
                
            except User.DoesNotExist:
                # Don't reveal if email exists
                messages.success(
                    request,
                    _('If an account with this email exists, a reset link has been sent.')
                )
                return redirect('accounts:login')
            
            except Exception as e:
                messages.error(
                    request,
                    _('Error sending reset email. Please try again later.')
                )
    else:
        form = CustomPasswordResetForm()
    
    context = {
        'form': form,
        'title': _('Reset Password')
    }
    
    return render(request, 'accounts/password_reset.html', context)


def password_reset_confirm_view(request, token):
    """Password reset confirmation view."""
    
    if request.user.is_authenticated:
        return redirect('core:home')
    
    try:
        reset_token = PasswordResetToken.objects.get(token=token)
        
        if not reset_token.is_valid():
            messages.error(request, _('Invalid or expired reset token.'))
            return redirect('accounts:password_reset')
        
        if request.method == 'POST':
            form = CustomSetPasswordForm(reset_token.user, request.POST)
            
            if form.is_valid():
                # Save new password
                user = form.save()
                
                # Mark token as used
                reset_token.used = True
                reset_token.save()
                
                messages.success(
                    request,
                    _('Password reset successful! You can now log in.')
                )
                
                return redirect('accounts:login')
        else:
            form = CustomSetPasswordForm(reset_token.user)
        
        context = {
            'form': form,
            'token': token,
            'title': _('Set New Password')
        }
        
        return render(request, 'accounts/password_reset_confirm.html', context)
        
    except PasswordResetToken.DoesNotExist:
        messages.error(request, _('Invalid reset token.'))
        return redirect('accounts:password_reset')


@login_required
@require_http_methods(["POST"])
def delete_account_view(request):
    """Delete user account view."""
    
    password = request.POST.get('password')
    
    if not password:
        messages.error(request, _('Password is required to delete account.'))
        return redirect('accounts:profile', username=request.user.username)
    
    # Verify password
    if not request.user.check_password(password):
        messages.error(request, _('Incorrect password.'))
        return redirect('accounts:profile', username=request.user.username)
    
    # Delete user account
    username = request.user.username
    
    with transaction.atomic():
        request.user.delete()
    
    messages.success(request, _('Account deleted successfully.'))
    return redirect('core:home')


@login_required
def dashboard_view(request):
    """User dashboard view."""
    
    userprofile, created = UserProfile.objects.get_or_create(user=request.user)
    
    # Get recent login attempts
    recent_logins = LoginAttempt.objects.filter(
        username=request.user.username,
        success=True
    ).order_by('-timestamp')[:5]
    
    context = {
        'profile': userprofile,
        'recent_logins': recent_logins,
        'completion_percentage': userprofile.get_completion_percentage(),
        'title': _('Dashboard')
    }
    
    return render(request, 'accounts/dashboard.html', context)


@login_required
def ajax_check_username(request):
    """AJAX view to check username availability."""
    
    username = request.GET.get('username', '').strip()
    
    if not username:
        return JsonResponse({'available': False, 'message': _('Username is required')})
    
    if len(username) < 3:
        return JsonResponse({'available': False, 'message': _('Username must be at least 3 characters')})
    
    # Check if username exists (excluding current user)
    exists = User.objects.filter(username=username).exclude(id=request.user.id).exists()
    
    if exists:
        return JsonResponse({'available': False, 'message': _('Username is already taken')})
    
    return JsonResponse({'available': True, 'message': _('Username is available')})


@login_required
def ajax_check_email(request):
    """AJAX view to check email availability."""
    
    email = request.GET.get('email', '').strip()
    
    if not email:
        return JsonResponse({'available': False, 'message': _('Email is required')})
    
    # Check if email exists (excluding current user)
    exists = User.objects.filter(email=email).exclude(id=request.user.id).exists()
    
    if exists:
        return JsonResponse({'available': False, 'message': _('Email is already registered')})
    
    return JsonResponse({'available': True, 'message': _('Email is available')})