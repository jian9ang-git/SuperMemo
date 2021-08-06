from django import forms
from django.db.models import Q
from memo.models import Theme, Section, Question


class LearningForm(forms.ModelForm):
    section = forms.CharField(max_length=500)
    theme = forms.CharField(max_length=500)
    question = forms.CharField(max_length=500)
    answer = forms.CharField(max_length=500)

    def clean(self):
        chd = self.changed_data
        cd = self.cleaned_data
        theme = self.initial.theme
        goal = self.instance.goal
        if 'section' in chd:
            Section.objects.create(name=cd['section'], goal=goal)
        elif 'theme' in chd:
            theme.set(last_used=False)
            Theme.objects.create(name=cd['theme'], section=cd['section'], goal=goal, last_used=True)

    class Meta:
        model = Question
        fields = ['section', 'theme', 'question', 'answer']
