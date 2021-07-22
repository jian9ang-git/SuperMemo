from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import User
from .models import Profile


class PersonalDataEditForm(forms.ModelForm):

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'Пользователь с логином {username} уже существует.')
        elif User.objects.filter(email=email).exists():
            raise forms.ValidationError(f'Пользователь с логином {email} уже существует.')
        return self.cleaned_data

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']

