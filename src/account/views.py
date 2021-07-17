from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, user_logged_in, user_logged_out
from django.views import View
from .forms import LoginForm, RegistrationForm
from memo.models import Profile, Goal, Question
from django.contrib.auth.models import User
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
    def get(self, request, *args, **kwargs):
        form = LoginForm()
        return render(request, 'login.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST or None)
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('memo:profile', username=username)
                    # return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('memo:home')


class RegistrationView(View):
    def get(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        return render(request, 'registration/registration.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST or None)
        if form.is_valid():
            new_user = form.save(commit=False)
            cd = form.cleaned_data
            new_user.username = cd['username']
            new_user.set_password(cd['password'])
            new_user.email = cd['email']
            new_user.save()
            #  --------------------------------------------------------------------------
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
            #  --------------------------------------------------------------------------
            new_user_id = new_user.id

            Profile.objects.create(
                id=new_user_id,
                user=new_user,
            )
            profile = Profile.objects.get(pk=new_user_id)
            username = cd['username']
            request.session['user_id'] = new_user_id
        else:
            return render(request, 'registration/registration.html', {'form': form})
        return redirect('memo:profile', username=username)


        #  return redirect('memo:profile', pk=cd['id'])



