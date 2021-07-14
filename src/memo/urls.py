from django.urls import path
from django.contrib.auth import login
from .views import HomePage, ProfilePage


urlpatterns = [
    # path('login/', user_login, name='login'),
    # path('password-change/', , name='password_change'),
    # path('password-change/done/', , name='password_change_done'),

    path('', HomePage.as_view(), name='home'),
    path('profile', ProfilePage.as_view(), name='profile'),

]