from django.shortcuts import render
from django.views import View


class HomePage(View):
    @staticmethod
    def get(request, *args, **kwargs):
        return render(request, 'home.html', {})

    def post(self, request, *args, **kwargs):
        return render(request, 'home.html', {})
