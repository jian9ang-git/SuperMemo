from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.views import View
from .forms import LoginForm, RegistrationForm
from memo.models import Profile, Goal, Question
from django.contrib.auth.decorators import login_required


# def user_login(request):
#     if request.method == 'POST':
#         form = LoginForm(request.POST)
#         if form.is_valid():
#             cd = form.cleaned_data
#             user = authenticate(username=cd['username'], password=cd['password'])
#             if user is not None:
#                 if user.is_active:
#                     login(request, user)
#                     return HttpResponse('Authenticated successfully')
#                 else:
#                     return HttpResponse('Disabled account')
#             else:
#                 return HttpResponse('Invalid login')
#     else:
#         form = LoginForm()
#     return render(request, 'login.html', {'form': form})


class LoginView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    @staticmethod
    def post(request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')


class RegistrationView(View):
    @staticmethod
    def get(request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        return render(request, 'registration/registration.html', {'form': form})

    @staticmethod
    def post(request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.username = form.cleaned_data['username']
            new_user.set_password(form.cleaned_data['password'])
            new_user.email = form.cleaned_data['email']
            new_user.save()
            new_user.set_password(form.cleaned_data['password'])

            Profile.objects.create(
                user=new_user,
            )
        # return render(request, 'home.html', {})
        return redirect('memo:home')

