from django.shortcuts import render
from django.views import View
from memo.models import Profile, Goal, Question


class HomePage(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


    def post(self, request, *args, **kwargs):
        return render(request, 'home.html', {})


class ProfilePage(View):

    def get(self, request, *args, **kwargs):
        profile = Profile.objects.get()
        return render(request, 'profile.html', {'profile': profile})


    def post(self, request, *args, **kwargs):
        return render(request, 'profile.html', {})
