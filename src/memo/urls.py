from django.urls import path
from django.contrib.auth import login
from .views import HomePage, ProfilePage
from django.conf.urls.static import static
from django.conf import settings



urlpatterns = [
    # path('login/', user_login, name='login'),
    # path('password-change/', , name='password_change'),
    # path('password-change/done/', , name='password_change_done'),

    path('', HomePage.as_view(), name='home'),
    path('profile/<str:username>', ProfilePage.as_view(), name='profile'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
