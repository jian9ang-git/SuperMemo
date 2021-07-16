from django.urls import path
from django.contrib.auth import login
# from .views import user_login
from .views import LoginView, RegistrationView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    # path('login/', user_login, name='login'),
    # path('password-change/', , name='password_change'),
    # path('password-change/done/', , name='password_change_done'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
    path('password-change/', auth_views.PasswordChangeView.as_view(), name='change'),
    path('password-change-done/', auth_views.PasswordChangeDoneView.as_view(), name='change_done'),
    path('password-reset/', auth_views.PasswordResetView.as_view(), name='reset_form'),
    path('password-reset-done/', auth_views.PasswordResetDoneView.as_view(), name='reset_done'),
    path('password-reset-confirm/', auth_views.PasswordResetConfirmView.as_view(), name='reset_done'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='reset_complete'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
