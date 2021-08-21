from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_POST

from memo.models import Profile, Goal, Question, Theme
from django.contrib.auth.models import User
from memo.forms import PersonalDataEditForm, AddGoalForm


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

        if profile.lessons.filter(active_lesson=True).exists():
            lesson = profile.lessons.get(active_lesson=True)
            request.session['active_lesson'] = True
            request.session['active_lesson_id'] = lesson.id
            return render(request, 'profile.html', {'profile': profile,
                                                    'username': kwargs['username'],
                                                    'goals': goals, 'lesson_id': lesson.id})

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
                                    instance=user)
        return render(request, 'edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PersonalDataEditForm(request.POST or None, instance=request.user)  # !!!!!!!!!!!1
        if form.is_valid():
            user = form.save(commit=True)
            return redirect('memo:profile', user.username)
        return render(request, 'edit.html', {'form': form})
