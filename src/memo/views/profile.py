from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_POST

from memo.models import Profile, Goal, Question, Theme, Section
from django.contrib.auth.models import User
from memo.forms import PersonalDataEditForm, AddGoalForm


class HomePage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})

    def post(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


class ProfilePage(View):
    def get(self, request, *args, **kwargs):
        profile = request.user.profile
        goals = profile.goals.all()

        return render(request, 'profile_page.html', {'profile': profile,
                                                     'goals': goals,
                                                     'username': kwargs['username']})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=request.session['user_id'])
        return render(request, 'profile_page.html', {})


class ProfilePageBasic(View):
    def get(self, request, *args, **kwargs):
        username = request.user.username
        if username:
            return redirect('memo:profile', username=username)
        else:
            return redirect('account:login')

    def post(self, request, *args, **kwargs):
        username = request.user.username
        if username:
            return redirect('memo:profile', username=username)
        else:
            return redirect('account:login')


class EditPage(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=request.session['user_id'])
        form = PersonalDataEditForm(initial={'username': user.username,
                                             'email': user.email,
                                             'first_name': user.first_name,
                                             'last_name': user.last_name},
                                    instance=user)
        return render(request, 'edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PersonalDataEditForm(request.POST or None, instance=request.user)
        if form.is_valid():
            user = form.save(commit=True)
            return redirect('memo:profile', user.username)
        return render(request, 'edit.html', {'form': form})
