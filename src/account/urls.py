from django.urls import path
from django.contrib.auth import login
# from .views import user_login
from .views import LoginView, RegistrationView, LogoutView
from django.conf.urls.static import static
from django.conf import settings


urlpatterns = [
    # path('login/', user_login, name='login'),
    # path('password-change/', , name='password_change'),
    # path('password-change/done/', , name='password_change_done'),

    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
