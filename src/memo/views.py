from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from memo.models import Profile, Goal, Question
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm, PasswordResetForm, SetPasswordForm, User
from .forms import PersonalDataEditForm


class HomePage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})

    def post(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


class ProfilePage(View):
    def get(self, request, *args, **kwargs):
        #  user = User.objects.filter(profile__id=request.session['user_id']).first()
        #  user = User.objects.filter(id=request.session['user_id']).first()
        user = User.objects.get(username=kwargs['username'])
        profile = user.profile
        return render(request, 'profile.html', {'profile': profile})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=request.session['user_id'])
        return render(request, 'profile.html', {})


class ProfilePageBasic(View):
    def get(self, request, *args, **kwargs):
        #  user = User.objects.filter(profile__id=request.session['user_id']).first()
        #  user = User.objects.filter(id=request.session['user_id']).first()
        user = User.objects.get(pk=request.session['user_id'])
        username = user.username
        profile = user.profile
        return redirect('memo:profile', username=username)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.session['user_id'])
        username = user.username
        profile = user.profile
        return redirect('memo:profile', username=username)


class EditPage(View):
    def get(self, request, *args, **kwargs):
        # profile = Profile.objects.get(pk=request.session['user_id'])
        # form = PersonalDataEditForm()
        # return render(request, 'edit.html', {'profile': profile, 'form': form})
        return render(request, 'edit.html')

    def post(self, request, *args, **kwargs):
        # user = User.objects.get(pk=request.session['user_id'])
        # form = PersonalDataEditForm(request.POST or None)
        # cd = form.cleaned_data
        # user.username = cd['username']
        # user.email = cd['email']
        # user.first_name = cd['first_name']
        # user.last_name = cd['last_name']
        # user.save()
        # return redirect('memo:profile', username=cd['username'])
        return render(request, 'edit.html')

# class EditPasswordPage(View):
#     def get(self, request, *args, **kwargs):
#         form = PasswordChangeForm()
#         return render(request, 'password_change_form.html', {'form': form})
#
#     def post(self, request, *args, **kwargs):
#         user = User.objects.get(pk=request.session['user_id'])
#         form = PasswordChangeForm(request.POST or None)
#         cd = form.cleaned_data
#         user.set_password(cd['password'])
#         user.save()
#         username = user.username
#         return render(request, 'registration/password_change_done.html', {'username': username})


# class EditPasswordDonePage(View):
#     def get(self, request, *args, **kwargs):
#         user = User.objects.get(pk=request.session['user_id'])
#         username = user.username
#         return render(request, 'registration/password_change_done.html', {'username': username})
#
#     def post(self, request, *args, **kwargs):
#         user = User.objects.get(pk=request.session['user_id'])
#         username = user.username
#         return render(request, 'registration/password_change_done.html', {'username': username})
