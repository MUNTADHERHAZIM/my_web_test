from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLs
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # Profile URLs
    path('profile/edit/', views.ProfileUpdateView.as_view(), name='profile_edit'),
    path('profile/', views.MyProfileView.as_view(), name='profile'),
    path('profile/<str:username>/', views.ProfileView.as_view(), name='profile_detail'),
    
    # Password management
    path('password/change/', views.change_password_view, name='password_change'),
    path('password/reset/', views.password_reset_request_view, name='password_reset'),
    path('password/reset/confirm/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),
    
    # Account management
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('delete/', views.delete_account_view, name='delete_account'),
    
    # AJAX endpoints
    path('ajax/check-username/', views.ajax_check_username, name='ajax_check_username'),
    path('ajax/check-email/', views.ajax_check_email, name='ajax_check_email'),
    
    # Built-in Django auth views (fallback)
    path('password_reset/', 
         auth_views.PasswordResetView.as_view(
             template_name='accounts/password_reset.html',
             email_template_name='accounts/password_reset_email.html',
             subject_template_name='accounts/password_reset_subject.txt',
             success_url='/accounts/password_reset/done/'
         ), 
         name='django_password_reset'),
    
    path('password_reset/done/', 
         auth_views.PasswordResetDoneView.as_view(
             template_name='accounts/password_reset_done.html'
         ), 
         name='django_password_reset_done'),
    
    path('reset/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(
             template_name='accounts/password_reset_confirm.html',
             success_url='/accounts/reset/done/'
         ), 
         name='django_password_reset_confirm'),
    
    path('reset/done/', 
         auth_views.PasswordResetCompleteView.as_view(
             template_name='accounts/password_reset_complete.html'
         ), 
         name='django_password_reset_complete'),
]