from django import forms
from django.db.models import Q
from memo.models import Theme, Section, Question


class LearningForm(forms.ModelForm):
    section = forms.CharField(max_length=500,
                              widget=forms.TextInput(attrs={'placeholder': 'Enter your first goal section here'}))
    theme = forms.CharField(max_length=500,
                            widget=forms.TextInput(attrs={'placeholder': 'Enter your first goal theme here'}))
    question = forms.CharField(max_length=500)
    answer = forms.CharField(max_length=500)

    # def clean(self):
    #     cd = self.cleaned_data
    #
    #     if self.instance.theme:
    #         last_used_theme = self.instance.theme
    #         if not Section.objects.get(name=cd['section']).exists():
    #             section = Section.objects.create(name=cd['section'], goal=last_used_theme.goal)
    #         else:
    #             section = Section.objects.get(name=cd['section'])
    #
    #         if not Theme.objects.get(name=cd['theme']).exists():
    #             last_used_theme.set(last_used=False)
    #
    #             Theme.objects.create(name=cd['theme'],
    #                                  section=section,
    #                                  goal=last_used_theme.goal,
    #                                  last_used=True)
    #         else:
    #             last_used_theme.set(last_used=False)
    #             last_used_theme = Theme.objects.get(name=cd['theme'])
    #             last_used_theme.set(last_used=True)
    #     else:
    #         section = Section.objects.create(name=cd['section'], goal=self.instance.goal)
    #         Theme.objects.create(name=cd['theme'], section=section, goal=self.instance.goal, last_used=True)

    class Meta:
        model = Question
        fields = ['section', 'theme', 'question', 'answer']


