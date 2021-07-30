from django import forms

from django.contrib.auth.models import User
from django.contrib.auth.forms import User
from .models import Profile, Goal, Question


class PersonalDataEditForm(forms.ModelForm):
    username = forms.CharField(required=False, min_length=3, max_length=150, )
    email = forms.EmailField(required=False)
    first_name = forms.CharField(required=False, min_length=3, max_length=150)
    last_name = forms.CharField(required=False, min_length=3, max_length=150)

    def clean(self):
        username = self.cleaned_data['username']
        email = self.cleaned_data['email']
        user_name = 'username'
        e_mail = 'email'
        chd = self.changed_data
        if User.objects.filter(username=username).exists() and user_name in chd:
            if User.objects.filter(email=email).exists() and e_mail in chd:
                raise forms.ValidationError(f'Логин {username} и почта {email} уже существуют.')
            raise forms.ValidationError(f'Пользователь с логином {username} уже существует.')

        elif User.objects.filter(email=email).exists() and e_mail in chd:
            raise forms.ValidationError(f'Пользователь с логином {email} уже существует.')

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name']


class AddGoalForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Name your goal'

    class Meta:
        model = Goal
        fields = ['name']
