from django import forms
from django.db.models import Q
from memo.models import Theme, Section, Question


# user_themes = Theme.objects.filter(Q())
# t_names = user_themes.name.all()
# user_sections = Section.objects.filter(Q)
# s_names = user_sections.name.all()
# i = [1,2,3,4,5]
# PRODUCT_QUANTITY_CHOICES = ((i, str(i)) for i in range(1, 21))


class LearningForm(forms.ModelForm):
    section = forms.CharField(max_length=500)
    theme = forms.CharField(max_length=500)
    question = forms.CharField(max_length=500)
    answer = forms.CharField(max_length=500)

    def clean(self):
        goal = self.goal
        chd = self.changed_data
        cd = self.cleaned_data
        if 'section' in chd:
            Section.objects.create(name=cd['section'], goal=goal)
        elif 'theme' in chd:
            Theme.objects.create(name=cd['theme'], section=cd['section'], goal=goal)

    class Meta:
        model = Question
        fields = ['section', 'theme', 'question', 'answer']


