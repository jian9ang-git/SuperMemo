from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_POST

from memo.models import Profile, Goal, Question, Theme
from django.contrib.auth.models import User
from .forms import PersonalDataEditForm, AddGoalForm


@require_POST
def add_goal(self, request, *args, **kwargs):
    form = AddGoalForm(request.POST or None)
    if form.is_valid():
        cd = form.cleaned_data
        user = request.user
        profile = user.profile
        goal = Goal.objects.create(name=cd['name'], profile=profile)
    return redirect('memo:profile_basic')


class HomePage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})

    def post(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


class ProfilePage(View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=kwargs['username'])
        profile = user.profile
        goals = profile.goals.all()
        return render(request, 'profile.html', {'profile': profile,
                                                'username': kwargs['username'],
                                                'goals': goals})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=request.session['user_id'])
        return render(request, 'profile.html', {})


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
                                    instance=request.user)
        return render(request, 'edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PersonalDataEditForm(request.POST or None, instance=request.user)
        if form.is_valid():
            user = form.save(commit=True)
            return redirect('memo:profile', user.username)
        return render(request, 'edit.html', {'form': form})


class GoalPage(View):
    def get(self, request, *args, **kwargs):
        goal = Goal.objects.get(pk=kwargs['goal_id'])
        goal_name = goal.name
        sections = goal.sections.all()
        themes = goal.themes.all()

        request.session['section'] = ''
        request.session['theme'] = ''

        return render(request, 'goal_page.html', {'sections': sections, 'themes': themes, 'goal': goal})

    def post(self, request, *args, **kwargs):
        pass