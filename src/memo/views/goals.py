from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views import View
from django.views.decorators.http import require_POST

from memo.models import Profile, Goal, Question, Theme
from django.contrib.auth.models import User
from memo.forms import AddGoalForm


class GoalPage(View):
    def get(self, request, *args, **kwargs):
        goal = Goal.objects.get(pk=kwargs['goal_id'])
        # user = request.user
        # active_lesson_id = is_active_lesson(user, goal)
        # if not active_lesson_id == False:
        #     request.session = active_lesson_id

        sections = goal.sections.all()
        themes = goal.themes.all()
        return render(request, 'goal_page.html', {'sections': sections, 'themes': themes, 'goal': goal})

    def post(self, request, *args, **kwargs):
        pass


class AddGoalPage(View):
    def get(self, request, *args, **kwargs):
        form = AddGoalForm
        return render(request, 'add_goal.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = AddGoalForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = request.user
            profile = user.profile
            goal = Goal.objects.create(name=cd['name'], profile=profile)
        return redirect('memo:profile_basic')
