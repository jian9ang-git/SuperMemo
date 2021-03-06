from django import forms
from django.db.models import Q
from memo.models import Theme, Question, Goal, Section


class LearningForm(forms.ModelForm):
    question = forms.CharField(max_length=500, required=True,
                               widget=forms.TextInput(attrs={'placeholder': 'Enter your question'}))
    answer = forms.CharField(max_length=500, required=True,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter the answer'}))

    class Meta:
        model = Question
        fields = ['question', 'answer']


class ChooseSectionForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Section.objects.all(), empty_label='Choose chapter')

    def __init__(self, *args, **kwargs):
        goal_id = kwargs.pop('goal_id', None)
        super(ChooseSectionForm, self).__init__(*args, **kwargs)

        if goal_id:
            self.fields['name'].queryset = Section.objects.filter(goal__id=goal_id)

    class Meta:
        model = Section
        fields = ['name']


class ChooseThemeForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Theme.objects.all(), empty_label='Choose theme')

    def __init__(self, *args, **kwargs):
        section_id = kwargs.pop('section_id', None)
        super(ChooseThemeForm, self).__init__(*args, **kwargs)

        if section_id:
            self.fields['name'].queryset = Theme.objects.filter(section__id=section_id)

    class Meta:
        model = Theme
        fields = ['name']


class AddSectionForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Name your section'

    class Meta:
        model = Section
        fields = ['name']


class AddThemeForm(forms.ModelForm):
    name = forms.CharField(required=True, min_length=3, max_length=150)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Name your theme'

    class Meta:
        model = Theme
        fields = ['name']
