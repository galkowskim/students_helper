from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import CustomLoginView, confirm_email, register, activate, password_reset_request, MainPageView, CustomPasswordResetConfirmView

urlpatterns = [
    path('', MainPageView.as_view(), name='main'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='base:login'), name='logout'),
    path('register/', register, name='register'),
    path('confirm_email/', confirm_email, name='confirm_email'),
    path('activate/<uidb64>/<token>/', activate, name='activate'),
    path("password_reset/", password_reset_request, name="password_reset"),
    path('password_reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='base/password/password_reset_done.html'),
         name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(template_name="base/password/password_reset_confirm.html"),
         name='password_reset_confirm'),
    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(template_name='base/password/password_reset_complete.html'),
         name='password_reset_complete'),
]
