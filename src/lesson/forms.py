from django import forms
from django.db.models import Q

from memo.models import Theme, Section


user_themes = Theme.objects.filter(Q())
t_names = user_themes.name.all()
user_sections = Section.objects.filter(Q)
s_names = user_sections.name.all()


class LearningForm(forms.ModelForm):
    section = forms.ChoiceField(choices=s_names, coerce=str)
    theme = forms.ChoiceField(choices=t_names, coerce=str)
    question = forms.CharField(max_length=500)
    answer = forms.CharField(max_length=500)
