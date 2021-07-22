from django.urls import path
from django.contrib.auth import login
# from .views import user_login
from .views import LoginView, RegistrationView, LogoutView
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('registration/', RegistrationView.as_view(), name='registration'),

    path('password-reset/',
         auth_views.PasswordResetView.as_view(
             template_name='registration/password_reset_form.html',
             subject_template_name='registration/password_reset_subject.txt',
             email_template_name='registration/password_reset_email.html',
             success_url='/account/password-reset/done/'),
         name='password_reset'),

    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(
             template_name='registration/password_reset_done.html'
         ),
         name='password_reset_done'),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(
             template_name='registration/password_reset_confirm.html',
             success_url='/account/reset/done/'),
         name='password_reset_confirm'),

    path('reset/done/',
         auth_views.PasswordResetCompleteView.as_view(
             template_name='registration/password_reset_complete.html',
         ),
         name='password_reset_complete'),

    # path('password-change/',
    #      auth_views.PasswordChangeView.as_view(
    #          template_name='registration/password_change_form.html',
    #          success_url='/account/password_change_done'),
    #      name='password_change'),
    #
    # path('password-change-done/',
    #      auth_views.PasswordChangeDoneView.as_view(
    #          template_name='registration/password_change_done.html'),
    #      name='password_change_done'),

    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# url(r'password_change/$',auth_views.PasswordChangeView.as_view(template_name='password_change.html',success_url='/accounts/password_change_done')),
# url(r'password_change_done/',auth_views.PasswordChangeDoneView.as_view(template_name='password_change_done.html')),
# url(r'password_reset/$',auth_views.PasswordResetView.as_view(template_name='password_reset.html',email_template_name='password_reset_email.html',subject_template_name='password_reset_subject.txt',success_url='/accounts/password_reset_done/',from_email='support@yoursite.ma')),
# url(r'password_reset_done/',auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html')),
# url(r'password_reset_confirm/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html',success_url='/accounts/password_reset_complete/')),
# url(r'password_reset_complete/',auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html')),
