from django.contrib.auth.urls import views as auth_views
from .views import register_user
from django.urls import path

urlpatterns  = [
    path('register/', register_user, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="accounts/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(template_name="accounts/logout.html"), name="logout"),
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"), name="password-reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('pasword-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name='password-reset-confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password-reset-complete'),
]