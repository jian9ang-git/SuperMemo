from django.shortcuts import render
from django.views import View
from memo.models import Profile, Goal, Question
from django.contrib.auth.models import User


class HomePage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})

    def post(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


class ProfilePage(View):

    def get(self, request, *args, **kwargs):
        user = User.objects.get(username=kwargs['username'])
        profile = Profile.objects.get(user=user)
        return render(request, 'profile.html', {'profile': profile})

    def post(self, request, *args, **kwargs):
        profile = Profile.objects.get(pk=request.session['new_user_id'])
        return render(request, 'profile.html', {})
