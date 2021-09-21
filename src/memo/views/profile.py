from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_POST

from memo.models import Profile, Goal, Question, Theme, Section
from django.contrib.auth.models import User
from memo.forms import PersonalDataEditForm, AddGoalForm


class HomePage(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


class ProfilePage(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        if User.objects.filter(profile__id=user.id).exists():  # Todo Нужно ли тестировать эту ветку?
            # profile = Profile.objects.get(user=request.user)
            profile = user.profile
        else:  # Todo И эту ветку?
            profile = Profile.objects.create(
                id=request.user.id,
                user=request.user
            )
        goals = profile.goals.all()

        return render(request, 'profile_page.html', {'profile': profile,
                                                     'goals': goals,
                                                     'username': kwargs['username']})


class ProfilePageBasic(View):
    def get(self, request, *args, **kwargs):
        username = request.user.username
        if username:
            return redirect('memo:profile', username=username)
        else:
            return redirect('account:login')


@method_decorator(login_required, name='dispatch')
class EditPage(View):
    def get(self, request, *args, **kwargs):
        user = request.user
        form = PersonalDataEditForm(initial={'username': user.username,
                                             'email': user.email,
                                             'first_name': user.first_name,
                                             'last_name': user.last_name},
                                    instance=user)
        return render(request, 'edit.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = PersonalDataEditForm(request.POST, instance=request.user)
        if form.is_valid():
            cd = form.cleaned_data  # Todo Добавил 58 и 59, т.к. без них ломался тест
            username = cd['username']  #
            user = form.save(commit=True)
            return redirect('memo:profile', username=username)
        return render(request, 'edit.html', {'form': form})
